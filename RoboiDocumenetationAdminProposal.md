
---

# **Roboi – Admin Panel (UI & Frontend Features Documentation)**

## 1. Overview

The **Admin Panel** of the Roboi project is responsible for:

* Managing users and role-based access
* Managing devices mapped to geographic hierarchy
* Configuring global and local settings
* Controlling KPI visibility and dashboard personalization
* Ensuring scalability for district, state, and country-level expansion

This document focuses on **UI-level features and frontend expectations**, with notes where backend validation is required.

---

## 2. Authentication & Onboarding

### 2.1 Admin Signup

**Purpose:** Allow initial admin or authorized users to onboard.

**UI Requirements:**

* Signup form with:

  * Name
  * Email
  * Password
  * Role (optional / auto-assigned)
* Theme selection (optional at signup)
* Logo upload (organization branding)
* Info fields (organization details)

**Notes:**

* Access must be **role-based**
* Some fields may be enabled/disabled depending on admin permissions

---

## 3. KPI Selection & Dashboard Configuration

### 3.1 KPI Selection

**Purpose:** Customize dashboard KPIs per admin or role.

**UI Features:**

* Multi-select KPI list
* Grouped KPIs (performance, device health, usage, etc.)
* Save KPI preferences per role/user
* Preview dashboard based on selected KPIs

---

## 4. User Management

### 4.1 Add Users

**UI Components:**

* Add User form:

  * Name
  * Email
  * Role
  * Assigned Geography (Country / State / City / Ro)
* Role-based access preview (read-only)

### 4.2 User List Table

**Columns:**

* Name
* Role
* Assigned Region
* Status (Active / Inactive)
* Actions (Edit / Disable)

---

## 5. Role & Geography Management

### 5.1 Role List

* View all available roles
* Assign permissions (checkbox-based)
* Map roles to:

  * Global
  * Country
  * State
  * City
  * Ro (Regional Office)

### 5.2 Geography Hierarchy (UI Flow)

```
Country
 └── State
     └── City
         └── Ro
```

**UI Requirements:**

* Cascading dropdowns
* Dynamic filtering based on selection
* Reusable components across forms

---

## 6. Settings Module

### 6.1 Global Settings

**Purpose:** Define default system behavior.

**Includes:**

* Default geography
* Default role
* Global configuration toggles
* Feature enable/disable flags

### 6.2 Local Settings

**Purpose:** Override global settings at lower levels.

**Supported Levels:**

* Country
* State
* City
* Ro

**UI Behavior:**

* Inherit global settings by default
* Override enabled with toggle
* Clear visual indicator of overridden values

---

## 7. Device Management

### 7.1 Add Device

**Form Fields:**

* Device ID
* Device Code
* Assigned Geography (Country → State → City → Ro)
* IP Address

**Important:**

* IP validation happens at **backend**
* UI should show validation errors clearly

---

### 7.2 Devices Page (Table View)

**Columns:**

* Device ID
* Device Code
* Location (District / City / State / Country)
* Ro
* Status
* Actions (Edit / Disable)

**Filters:**

* Country
* State
* City
* Ro
* Status

---

## 8. Admin Controls

### 8.1 Admin Checkboxes / Permissions

**UI Features:**

* Checkbox-based permission assignment
* Permissions include:

  * Users Table
  * Devices Table
  * Global List
  * Country
  * State
  * City
  * Ro
  * Settings

**Behavior:**

* Permissions dynamically enable/disable UI sections
* Reusable permission component

---

## 9. Theme Management

### 9.1 Dark / Light Theme

**Default:** Light Theme

**UI Features:**

* Theme toggle (header or settings)
* Persist user preference
* Theme applied across:

  * Tables
  * Forms
  * Modals
  * Dashboard

---

## 10. Reusability & Frontend Notes

### 10.1 Reusable Components

* Cascading geography selector
* Table with filters & pagination
* Role permission checkbox group
* Theme toggle
* Settings override panel

### 10.2 Frontend Expectations

* Role-based UI rendering
* Clean separation of:

  * Global configs
  * Local overrides
* Scalable layout for future KPIs & visualizations

---

## 11. Backend Dependencies (Awareness Only)

Frontend should assume:

* IP validation handled server-side
* Role permissions enforced server-side
* Geography hierarchy fetched dynamically
* Settings inheritance logic supported by APIs

---

## 12. Summary

The Roboi Admin Panel UI is designed to be:

* **Scalable**
* **Role-driven**
* **Geography-aware**
* **Configurable at multiple levels**
* **Dashboard-centric with KPI customization**

This documentation can directly guide:

* UI wireframing
* Component design
* API contract discussions
* Sprint planning

---

