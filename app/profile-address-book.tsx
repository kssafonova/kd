"use client";

import { useEffect } from "react";

type LegacyProfile = {
  name?: string;
  surname?: string;
  email?: string;
  phone?: string;
  city?: string;
  address?: string;
};

type DeliveryAddress = {
  id: string;
  label: string;
  city: string;
  address: string;
  flat: string;
  comment: string;
};

type DeliveryRecipient = {
  id: string;
  name: string;
  surname: string;
  phone: string;
  email: string;
  addresses: DeliveryAddress[];
  defaultAddressId?: string;
};

type AddressBook = {
  version: 1;
  recipients: DeliveryRecipient[];
  defaultRecipientId?: string;
};

const BOOK_KEY = "kultura-address-book-v1";
const PROFILE_KEY = "kultura-profile";

const uid = (prefix: string) => `${prefix}-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;

const escapeHtml = (value: string | undefined) => String(value ?? "")
  .replaceAll("&", "&amp;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;")
  .replaceAll('"', "&quot;")
  .replaceAll("'", "&#039;");

const readLegacyProfile = (): LegacyProfile | null => {
  try {
    const raw = localStorage.getItem(PROFILE_KEY);
    return raw ? JSON.parse(raw) as LegacyProfile : null;
  } catch {
    return null;
  }
};

const makeLegacyBook = (): AddressBook => {
  const profile = readLegacyProfile();
  if (!profile) return { version: 1, recipients: [] };

  const recipientId = uid("recipient");
  const addressId = uid("address");
  const hasAddress = Boolean(profile.city?.trim() || profile.address?.trim());
  const recipient: DeliveryRecipient = {
    id: recipientId,
    name: profile.name ?? "",
    surname: profile.surname ?? "",
    phone: profile.phone ?? "",
    email: profile.email ?? "",
    addresses: hasAddress ? [{
      id: addressId,
      label: "Основной адрес",
      city: profile.city || "Москва",
      address: profile.address ?? "",
      flat: "",
      comment: "",
    }] : [],
    defaultAddressId: hasAddress ? addressId : undefined,
  };
  return { version: 1, recipients: [recipient], defaultRecipientId: recipientId };
};

const normalizeBook = (value: unknown): AddressBook => {
  const source = value && typeof value === "object" ? value as Partial<AddressBook> : {};
  const recipients = Array.isArray(source.recipients) ? source.recipients.map((row) => {
    const recipient = row as Partial<DeliveryRecipient>;
    const addresses = Array.isArray(recipient.addresses) ? recipient.addresses.map((addressRow) => {
      const address = addressRow as Partial<DeliveryAddress>;
      return {
        id: address.id || uid("address"),
        label: address.label || "Адрес доставки",
        city: address.city || "Москва",
        address: address.address || "",
        flat: address.flat || "",
        comment: address.comment || "",
      };
    }) : [];
    const defaultAddressId = addresses.some((address) => address.id === recipient.defaultAddressId)
      ? recipient.defaultAddressId
      : addresses[0]?.id;
    return {
      id: recipient.id || uid("recipient"),
      name: recipient.name || "",
      surname: recipient.surname || "",
      phone: recipient.phone || "",
      email: recipient.email || "",
      addresses,
      defaultAddressId,
    };
  }) : [];
  const defaultRecipientId = recipients.some((recipient) => recipient.id === source.defaultRecipientId)
    ? source.defaultRecipientId
    : recipients[0]?.id;
  return { version: 1, recipients, defaultRecipientId };
};

const loadBook = (): AddressBook => {
  try {
    const raw = localStorage.getItem(BOOK_KEY);
    if (raw) return normalizeBook(JSON.parse(raw));
  } catch {}
  const migrated = makeLegacyBook();
  try { localStorage.setItem(BOOK_KEY, JSON.stringify(migrated)); } catch {}
  return migrated;
};

const saveBook = (book: AddressBook) => {
  const normalized = normalizeBook(book);
  try { localStorage.setItem(BOOK_KEY, JSON.stringify(normalized)); } catch {}
  window.dispatchEvent(new CustomEvent("kultura-address-book-change", { detail: normalized }));
};

const recipientName = (recipient: DeliveryRecipient) =>
  [recipient.name, recipient.surname].filter(Boolean).join(" ") || "Получатель";

const addressLine = (address: DeliveryAddress) =>
  [address.city, address.address, address.flat ? `кв. ${address.flat}` : ""].filter(Boolean).join(", ");

const setReactInput = (input: HTMLInputElement | null, value: string) => {
  if (!input) return;
  const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value")?.set;
  setter?.call(input, value);
  input.dispatchEvent(new Event("input", { bubbles: true }));
  input.dispatchEvent(new Event("change", { bubbles: true }));
};

const fillCheckout = (overlay: HTMLElement, recipient: DeliveryRecipient, address?: DeliveryAddress) => {
  setReactInput(overlay.querySelector<HTMLInputElement>('input[name="name"]'), recipient.name);
  setReactInput(overlay.querySelector<HTMLInputElement>('input[name="surname"]'), recipient.surname);
  setReactInput(overlay.querySelector<HTMLInputElement>('input[name="email"]'), recipient.email);
  setReactInput(overlay.querySelector<HTMLInputElement>('input[name="phone"]'), recipient.phone);
  if (address) {
    setReactInput(overlay.querySelector<HTMLInputElement>('input[name="city"]'), address.city);
    setReactInput(overlay.querySelector<HTMLInputElement>('input[name="address"]'), address.address);
    setReactInput(overlay.querySelector<HTMLInputElement>('input[name="flat"]'), address.flat);
    setReactInput(overlay.querySelector<HTMLInputElement>('input[name="comment"]'), address.comment);
  }
};

function enhanceAccount(profile: HTMLElement) {
  if (profile.querySelector("[data-address-book-root]")) return;
  profile.classList.add("profile-book-enhanced");

  const root = document.createElement("section");
  root.dataset.addressBookRoot = "true";
  root.className = "profile-address-book";
  const fields = profile.querySelector(".account-fields");
  fields?.insertAdjacentElement("afterend", root);

  let editingRecipientId: string | null = null;
  let editingAddressRecipientId: string | null = null;
  let editingAddressId: string | null = null;

  const renderRecipientEditor = (book: AddressBook) => {
    if (!editingRecipientId) return "";
    const recipient = editingRecipientId === "new"
      ? { id: "", name: "", surname: "", phone: "", email: "", addresses: [] } as DeliveryRecipient
      : book.recipients.find((item) => item.id === editingRecipientId);
    if (!recipient) return "";
    return `<form class="profile-book-editor" data-recipient-form>
      <div class="profile-book-editor-head"><strong>${editingRecipientId === "new" ? "Новый получатель" : "Редактировать получателя"}</strong><button type="button" data-cancel-recipient aria-label="Закрыть">×</button></div>
      <div class="profile-book-fields">
        <label><span>Имя</span><input name="name" value="${escapeHtml(recipient.name)}" required></label>
        <label><span>Фамилия</span><input name="surname" value="${escapeHtml(recipient.surname)}"></label>
        <label><span>Телефон</span><input name="phone" type="tel" value="${escapeHtml(recipient.phone)}" required></label>
        <label><span>Email</span><input name="email" type="email" value="${escapeHtml(recipient.email)}"></label>
      </div>
      <button class="profile-book-save" type="submit">СОХРАНИТЬ ПОЛУЧАТЕЛЯ</button>
    </form>`;
  };

  const renderAddressEditor = (book: AddressBook) => {
    if (!editingAddressRecipientId) return "";
    const recipient = book.recipients.find((item) => item.id === editingAddressRecipientId);
    if (!recipient) return "";
    const address = editingAddressId && editingAddressId !== "new"
      ? recipient.addresses.find((item) => item.id === editingAddressId)
      : undefined;
    return `<form class="profile-book-editor address-editor" data-address-form data-recipient-id="${recipient.id}">
      <div class="profile-book-editor-head"><strong>${address ? "Редактировать адрес" : "Новый адрес"}</strong><button type="button" data-cancel-address aria-label="Закрыть">×</button></div>
      <div class="profile-book-fields address-fields">
        <label><span>Название</span><input name="label" value="${escapeHtml(address?.label || "Дом")}" placeholder="Дом, Работа, Дача"></label>
        <label><span>Город</span><input name="city" value="${escapeHtml(address?.city || "Москва")}" required></label>
        <label class="wide"><span>Улица и дом</span><input name="address" value="${escapeHtml(address?.address)}" required></label>
        <label><span>Квартира / офис</span><input name="flat" value="${escapeHtml(address?.flat)}"></label>
        <label><span>Комментарий курьеру</span><input name="comment" value="${escapeHtml(address?.comment)}"></label>
      </div>
      <button class="profile-book-save" type="submit">СОХРАНИТЬ АДРЕС</button>
    </form>`;
  };

  const render = () => {
    const book = loadBook();
    root.innerHTML = `<div class="profile-book-heading">
      <div><small>ДОСТАВКА</small><h3>Получатели и адреса</h3><p>Сохраните несколько получателей и адресов, чтобы выбирать их при оформлении заказа.</p></div>
      <button type="button" data-add-recipient>+ ПОЛУЧАТЕЛЬ</button>
    </div>
    <div class="profile-book-list">
      ${book.recipients.length ? book.recipients.map((recipient) => {
        const isDefault = recipient.id === book.defaultRecipientId;
        return `<article class="profile-recipient-card ${isDefault ? "is-default" : ""}" data-recipient-id="${recipient.id}">
          <header>
            <div><span class="profile-recipient-avatar">${escapeHtml((recipient.name || "П").slice(0, 1).toUpperCase())}</span><div><strong>${escapeHtml(recipientName(recipient))}</strong><small>${escapeHtml(recipient.phone || recipient.email || "Контакты не указаны")}</small></div></div>
            <button type="button" data-edit-recipient="${recipient.id}">ИЗМЕНИТЬ</button>
          </header>
          <div class="profile-recipient-actions">
            ${isDefault ? '<span class="profile-default-badge">ПОЛУЧАТЕЛЬ ПО УМОЛЧАНИЮ</span>' : `<button type="button" data-default-recipient="${recipient.id}">Сделать основным</button>`}
            ${book.recipients.length > 1 ? `<button type="button" class="danger" data-remove-recipient="${recipient.id}">Удалить</button>` : ""}
          </div>
          <div class="profile-addresses">
            ${recipient.addresses.length ? recipient.addresses.map((address) => {
              const isDefaultAddress = address.id === recipient.defaultAddressId;
              return `<div class="profile-address-card ${isDefaultAddress ? "is-default" : ""}">
                <button type="button" class="profile-address-main" data-default-address="${recipient.id}|${address.id}">
                  <span class="profile-address-radio">${isDefaultAddress ? "✓" : ""}</span>
                  <span><strong>${escapeHtml(address.label || "Адрес доставки")}</strong><small>${escapeHtml(addressLine(address))}</small>${address.comment ? `<em>${escapeHtml(address.comment)}</em>` : ""}</span>
                </button>
                <div><button type="button" data-edit-address="${recipient.id}|${address.id}">Изменить</button><button type="button" data-remove-address="${recipient.id}|${address.id}">Удалить</button></div>
              </div>`;
            }).join("") : '<p class="profile-address-empty">Адресов пока нет.</p>'}
            <button type="button" class="profile-add-address" data-add-address="${recipient.id}">+ ДОБАВИТЬ АДРЕС</button>
          </div>
        </article>`;
      }).join("") : '<div class="profile-book-empty"><strong>Добавьте первого получателя</strong><span>Его контакты и адрес можно будет выбрать в checkout.</span></div>'}
    </div>
    ${renderRecipientEditor(book)}
    ${renderAddressEditor(book)}`;
  };

  root.addEventListener("click", (event) => {
    const target = (event.target as HTMLElement).closest<HTMLElement>("button");
    if (!target) return;
    const book = loadBook();

    if (target.hasAttribute("data-add-recipient")) {
      editingRecipientId = "new";
      editingAddressRecipientId = null;
      editingAddressId = null;
      render();
      return;
    }
    if (target.dataset.editRecipient) {
      editingRecipientId = target.dataset.editRecipient;
      editingAddressRecipientId = null;
      editingAddressId = null;
      render();
      return;
    }
    if (target.hasAttribute("data-cancel-recipient")) {
      editingRecipientId = null;
      render();
      return;
    }
    if (target.dataset.defaultRecipient) {
      book.defaultRecipientId = target.dataset.defaultRecipient;
      saveBook(book);
      render();
      return;
    }
    if (target.dataset.removeRecipient) {
      const id = target.dataset.removeRecipient;
      if (!window.confirm("Удалить получателя и его сохранённые адреса?")) return;
      book.recipients = book.recipients.filter((recipient) => recipient.id !== id);
      if (book.defaultRecipientId === id) book.defaultRecipientId = book.recipients[0]?.id;
      saveBook(book);
      render();
      return;
    }
    if (target.dataset.addAddress) {
      editingAddressRecipientId = target.dataset.addAddress;
      editingAddressId = "new";
      editingRecipientId = null;
      render();
      return;
    }
    if (target.dataset.editAddress) {
      const [recipientId, addressId] = target.dataset.editAddress.split("|");
      editingAddressRecipientId = recipientId;
      editingAddressId = addressId;
      editingRecipientId = null;
      render();
      return;
    }
    if (target.hasAttribute("data-cancel-address")) {
      editingAddressRecipientId = null;
      editingAddressId = null;
      render();
      return;
    }
    if (target.dataset.defaultAddress) {
      const [recipientId, addressId] = target.dataset.defaultAddress.split("|");
      const recipient = book.recipients.find((item) => item.id === recipientId);
      if (recipient) recipient.defaultAddressId = addressId;
      saveBook(book);
      render();
      return;
    }
    if (target.dataset.removeAddress) {
      const [recipientId, addressId] = target.dataset.removeAddress.split("|");
      const recipient = book.recipients.find((item) => item.id === recipientId);
      if (!recipient) return;
      recipient.addresses = recipient.addresses.filter((address) => address.id !== addressId);
      if (recipient.defaultAddressId === addressId) recipient.defaultAddressId = recipient.addresses[0]?.id;
      saveBook(book);
      render();
    }
  });

  root.addEventListener("submit", (event) => {
    event.preventDefault();
    const form = event.target as HTMLFormElement;
    const data = new FormData(form);
    const book = loadBook();

    if (form.matches("[data-recipient-form]")) {
      const next = {
        name: String(data.get("name") || "").trim(),
        surname: String(data.get("surname") || "").trim(),
        phone: String(data.get("phone") || "").trim(),
        email: String(data.get("email") || "").trim(),
      };
      if (!next.name || !next.phone) return;
      if (editingRecipientId === "new") {
        const id = uid("recipient");
        book.recipients.push({ id, ...next, addresses: [] });
        if (!book.defaultRecipientId) book.defaultRecipientId = id;
      } else {
        const recipient = book.recipients.find((item) => item.id === editingRecipientId);
        if (recipient) Object.assign(recipient, next);
      }
      editingRecipientId = null;
      saveBook(book);
      render();
      return;
    }

    if (form.matches("[data-address-form]")) {
      const recipientId = form.dataset.recipientId;
      const recipient = book.recipients.find((item) => item.id === recipientId);
      if (!recipient) return;
      const next = {
        label: String(data.get("label") || "Адрес доставки").trim() || "Адрес доставки",
        city: String(data.get("city") || "").trim(),
        address: String(data.get("address") || "").trim(),
        flat: String(data.get("flat") || "").trim(),
        comment: String(data.get("comment") || "").trim(),
      };
      if (!next.city || !next.address) return;
      if (editingAddressId === "new") {
        const id = uid("address");
        recipient.addresses.push({ id, ...next });
        if (!recipient.defaultAddressId) recipient.defaultAddressId = id;
      } else {
        const address = recipient.addresses.find((item) => item.id === editingAddressId);
        if (address) Object.assign(address, next);
      }
      editingAddressRecipientId = null;
      editingAddressId = null;
      saveBook(book);
      render();
    }
  });

  render();
}

function enhanceCheckout(overlay: HTMLElement) {
  const contactSection = overlay.querySelector<HTMLElement>(".checkout-section");
  const checkoutFields = contactSection?.querySelector<HTMLElement>(".checkout-fields");
  if (!contactSection || !checkoutFields || contactSection.querySelector("[data-checkout-address-book]")) return;
  const book = loadBook();
  if (!book.recipients.length) return;

  const root = document.createElement("div");
  root.dataset.checkoutAddressBook = "true";
  root.className = "checkout-address-book";
  checkoutFields.insertAdjacentElement("beforebegin", root);

  let recipientId = book.defaultRecipientId || book.recipients[0].id;
  let addressId = book.recipients.find((item) => item.id === recipientId)?.defaultAddressId;

  const render = (apply = false) => {
    const currentBook = loadBook();
    const recipient = currentBook.recipients.find((item) => item.id === recipientId) || currentBook.recipients[0];
    if (!recipient) return;
    recipientId = recipient.id;
    const address = recipient.addresses.find((item) => item.id === addressId)
      || recipient.addresses.find((item) => item.id === recipient.defaultAddressId)
      || recipient.addresses[0];
    addressId = address?.id;

    root.innerHTML = `<div class="checkout-saved-head"><div><small>СОХРАНЁННЫЕ ДАННЫЕ</small><strong>Кому доставить?</strong></div><span>${currentBook.recipients.length} получ.</span></div>
      <div class="checkout-recipient-tabs">${currentBook.recipients.map((item) => `<button type="button" class="${item.id === recipientId ? "active" : ""}" data-checkout-recipient="${item.id}"><strong>${escapeHtml(recipientName(item))}</strong><small>${escapeHtml(item.phone)}</small></button>`).join("")}</div>
      ${recipient.addresses.length ? `<div class="checkout-address-tabs"><p>Адрес доставки</p>${recipient.addresses.map((item) => `<button type="button" class="${item.id === addressId ? "active" : ""}" data-checkout-address="${item.id}"><span>${item.id === addressId ? "✓" : ""}</span><b>${escapeHtml(item.label)}</b><small>${escapeHtml(addressLine(item))}</small></button>`).join("")}</div>` : '<div class="checkout-no-address">Для этого получателя адрес ещё не сохранён — заполните его ниже.</div>'}`;

    if (apply) fillCheckout(overlay, recipient, address);
  };

  root.addEventListener("click", (event) => {
    const target = (event.target as HTMLElement).closest<HTMLButtonElement>("button");
    if (!target) return;
    if (target.dataset.checkoutRecipient) {
      recipientId = target.dataset.checkoutRecipient;
      const recipient = loadBook().recipients.find((item) => item.id === recipientId);
      addressId = recipient?.defaultAddressId || recipient?.addresses[0]?.id;
      render(true);
      return;
    }
    if (target.dataset.checkoutAddress) {
      addressId = target.dataset.checkoutAddress;
      render(true);
    }
  });

  render(true);
}

export function ProfileAddressBookEnhancer() {
  useEffect(() => {
    const scan = () => {
      document.querySelectorAll<HTMLElement>(".auth-profile").forEach(enhanceAccount);
      document.querySelectorAll<HTMLElement>(".checkout-overlay").forEach(enhanceCheckout);
    };
    scan();
    const observer = new MutationObserver(scan);
    observer.observe(document.body, { childList: true, subtree: true });
    const onChange = () => {
      document.querySelectorAll<HTMLElement>(".checkout-overlay [data-checkout-address-book]").forEach((node) => node.remove());
      scan();
    };
    window.addEventListener("kultura-address-book-change", onChange);
    return () => {
      observer.disconnect();
      window.removeEventListener("kultura-address-book-change", onChange);
    };
  }, []);
  return null;
}
