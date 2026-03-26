# 📡 Custom-Made CMS — Live Analysis Report
## Source: Xibo CMS Instances (Ultra v3.0.1 & Swift v4.1.2)

---

## 🔍 EXECUTIVE SUMMARY

Both CMS instances are **Digital Signage Management Platforms** (DSPs) — cloud-based systems that:
- Manage a fleet of remote display screens/players
- Schedule media content (images, videos, HTML, data feeds) to those screens
- Track playback proof, bandwidth, and uptime
- Allow multi-tenant user management with granular permissions

| Property | Ultra CMS | Swift CMS |
|---|---|---|
| URL | `https://ultra.ngage.services` | `https://swift.ngage.services` |
| Version | Xibo 3.0.1 | Xibo 4.1.2 |
| Displays | 8,457 | 0 (fresh/test) |
| Library Size | 101.5 GiB | 8.3 GiB |
| Users | 95 | 2 |
| Now Showing | 788 | 0 |
| UI Style | Top navbar (Bootstrap 3) | Left sidebar (Bootstrap 5) |

---

## 📊 SECTION 1 — DASHBOARD

**URL**: `/statusdashboard`

### Stats Tiles (top row)
| Tile | Description |
|---|---|
| Displays | Total registered display players |
| Library Size | Total uploaded file storage (GiB) |
| Users | Registered CMS user count |
| Now Showing | Currently active playing layouts |

### Charts
- **Bandwidth Usage (TiB)** — Bar chart, monthly, per domain
- **Library Usage** — Pie chart broken down by media type:
  - Video GiB
  - Image GiB
  - PDF GiB
  - Audio GiB
  - HTML Package GiB
  - Font GiB
  - Generic File GiB
  - Module GiB
  - Player Software GiB
  - PowerPoint GiB

### Tables
- **Display Activity** — shows display name, logged-in status (✓/✗), authorized status
- **Latest News** — pulls from Xibo blog RSS feed

---

## 🖥️ SECTION 2 — DISPLAYS MANAGEMENT

### 2.1 Displays List
**URL**: `/display/view`

**Table Columns**: ID, Display Name, Status (icon: tick/warning/error), Authorized?, Default Layout, Logged In?, Last Accessed, MAC Address, IP Address, Client Version, Display Profile, Tags, Created Date

**Row Actions** (via kebab menu):
- Edit
- Delete
- Authorize / Revoke Authorization
- Default Layout (set)
- Manage (opens display-level timeline)
- Request Screenshot
- Collect Now (force sync)
- Send Command
- Wake On LAN
- Move to another CMS
- Assign to Display Group

**Filters**: Name, Tags, Authorized, Logged In, Status

**Edit Display — Tab Structure**:
| Tab | Fields |
|---|---|
| General | Display Name, Default Layout, Orientation, Description, Tags |
| Location | Latitude, Longitude, Address, Timezone |
| Maintenance | Enable Maintenance, Screen Schedule (email alerts) |
| Wake On LAN | MAC Address, Port, Wake Schedule |
| Profile Settings | Collection Interval, Download Window, Update Window |
| Remote | VNC Host, VNC Port |
| Advanced | Custom ID, Bandwidth Limit per month, Audit enabled? |

---

### 2.2 Display Groups
**URL**: `/displaygroup/view`

**Columns**: ID, Group Name, Description, Is Dynamic?, Criteria (dynamic filter rule), Tags

**Dynamic Groups**: Filter displays by tag/profile automatically — no manual assignment.

**Row Actions**: Edit, Delete, Members, Permissions, Send Command, Collect Now

---

### 2.3 Display Setting Profiles
**URL**: `/displayprofile/view`

**Purpose**: Hardware-level configuration templates applied to player types.

**Supported Client Types**:
- Android
- Windows
- Linux
- webOS (LG)
- Tizen (Samsung)
- SSSP (Samsung SSP)

**Key Profile Settings**:
- Collection Interval (how often player fetches new content, seconds)
- Download & Update Windows (time ranges)
- Screen Dimensions, Orientation
- Log Level, Stats Enabled
- Proxy settings

---

### 2.4 Sync Groups
**URL**: `/syncgroup/view`

Purpose: Synchronize playback across multiple screens simultaneously (video walls, multi-panel displays). Uses a "leader" display to broadcast timing to "followers."

---

## 🎨 SECTION 3 — DESIGN / CONTENT CREATION

### 3.1 Layouts
**URL**: `/layout/view`

**Table Columns**: ID, Layout Name, Duration, Owner, Tags, Status (valid/draft/retired), Background Color, Width, Height, Created Date, Modified Date

**Row Actions**:
| Action | Description |
|---|---|
| Design | Opens the visual layout editor |
| Preview | Fullscreen browser preview |
| Edit | Edit metadata (name, tags, resolution) |
| Copy | Duplicate layout |
| Delete | Remove permanently |
| Retire | Soft-delete (keeps history) |
| Export | Download as ZIP |
| Assign to Campaign | Link to a campaign |
| Tag | Add/remove tags |
| Permissions | Set user/group access level |

**Import**: Upload an exported ZIP to restore/share layouts.

---

### 3.2 Layout Designer
**URL**: `/layout/designer/{id}`

This is the CORE feature — a visual canvas with the following panels:

#### Canvas
- Drag-and-drop region placement
- Resizable regions
- Z-order/layer control
- Background image/color picker

#### Toolbar / Widget Library
Full list of available widgets:
| Category | Widgets |
|---|---|
| **Media** | Image, Video, Audio, PDF, Local Video |
| **Streaming** | HLS Stream |
| **Web** | Web Page, Embedded HTML, HTML Package |
| **Dynamic Data** | Ticker (RSS/Text), DataSet View, DataSet Ticker |
| **Info/Tools** | Text, Digital Clock, Analogue Clock, Countdown |
| **Weather** | Weather (powered by Open Weather Map) |
| **Social** | Twitter/X Feed |
| **Interactive** | Shell Command |
| **Advanced** | Sub-Playlist, Notifications |
| **Menu** | Menu Board widget |

#### Region Properties Panel
- Region Name
- Loop (yes/no)
- Transitions: In and Out (Fly, Fade)
- Duration

#### Widget Properties Panel
- Duration (seconds, or inherit from playlist)
- Expiry (not display after date)
- Stats collection enabled?

#### Timeline Panel (bottom)
- Horizontal scroll sequence of widgets in a region
- Drag to reorder
- Duration shown per widget

#### Layout Properties Panel
- Name, Tags, Folder
- Resolution (width × height)
- Background: color picker OR image from library
- Sharing/Permissions

---

### 3.3 Playlists
**URL**: `/playlist/view`

**Purpose**: Reusable content lists (not tied to a layout/region). Can be embedded into layouts via "Sub-Playlist" widget.

**Table Columns**: ID, Name, Duration, Owner, Tags, Created Date

**Row Actions**: Edit, Delete, Timeline Editor, Permissions, Copy

---

### 3.4 Templates
**URL**: `/template/view`

**Purpose**: Save a layout as a reusable template. Includes layout structure + regions but no media.

**Columns**: ID, Name, Tags, Owner, Resolution

**Actions**: Edit, Delete, Create Layout from Template, Export

---

### 3.5 Resolutions
**URL**: `/resolution/view`

**Purpose**: Manage supported screen resolutions.

**Default Resolutions**: HD (1920×1080), 4K (3840×2160), Portrait (1080×1920), etc.

**Custom**: Add any W×H pixel resolution.

---

### 3.6 Campaigns
**URL**: `/campaign/view`

**Two types**:
1. **List**: Ordered sequence of layouts that plays in loop
2. **Ad Campaign**: Uses Share of Voice (SoV) % to control how often a layout plays relative to others

**Table Columns**: ID, Campaign Name, Type (List/Ad), Layouts assigned, Created Date

---

## 📁 SECTION 4 — LIBRARY & DATA

### 4.1 Media Library
**URL**: `/library/view`

**Upload Types**:
| Type | Extensions |
|---|---|
| Image | JPG, PNG, GIF, SVG, WEBP |
| Video | MP4, WEBM, AVI, MOV |
| Audio | MP3, OGG, WAV |
| PDF | PDF |
| HTML Package | ZIP (containing index.html) |
| Font | TTF, OTF |
| Generic File | Any file served as-is |
| PowerPoint | PPT, PPTX |
| Player Software | APK, EXE installers |

**Table Columns**: ID, Name, Owner, Type, Duration, File Size, Revised?, Used In (count), Tags, Modified Date

**Row Actions**:
| Action | Description |
|---|---|
| Edit | Rename, re-tag |
| Delete | Remove (warns if in use) |
| Download | Download original file |
| Replace | Swap file keeping all assignments |
| Retire | Soft-delete |
| Copy | Duplicate with new name |
| Usage Report | Show all layouts/playlists using this file |
| Set Expiry | Auto-remove after date |
| Permissions | Set user/group access |

**Tidy Library**: Admin tool to remove unused/orphaned files.

---

### 4.2 DataSets
**URL**: `/dataset/view`

**Purpose**: Internal mini-database tables used to power dynamic content widgets (Ticker, DataSet View).

**Table Columns (Datasets list)**: ID, Name, Description, Owner, Tags

**DataSet Configuration**:
- Define columns (type: Text, Number, Date, External Image, Library Image, HTML)
- Manual row entry (spreadsheet-style)
- CSV Import
- Remote DataSet: auto-fetch JSON/CSV from URL on schedule

**Row Ordering**: Custom order for how rows display in widgets.

---

### 4.3 Menu Boards
**URL**: `/menuboard/view`

**Purpose** (v4.x only): Specialized layout module for digital restaurant/retail menus.

**Structure**: Menu Board → Categories → Products

**Product Fields**: Name, Price, Allergen Info, Image, Description, Availability

---

## 📅 SECTION 5 — SCHEDULING

### 5.1 Schedule Calendar
**URL**: `/schedule/view`

**Calendar Views**: Month, Week, Day, Agenda, Grid

**Event Types**:
| Type | Description |
|---|---|
| Layout | Play a specific layout |
| Campaign | Play a campaign (ordered list or SoV) |
| Overlay | Plays on top of existing layout (alerts, tickers) |
| Interrupt | Pre-empts the current schedule at priority |
| Command | Execute a shell/system command |

**Add Event Form Fields**:
| Field | Options |
|---|---|
| Event Type | Layout / Campaign / Overlay / Command / Interrupt |
| Display/Group | Which screens |
| Layout/Campaign | What to play |
| Start/End Date | Date-time pickers |
| Is Repeating? | Yes/No |
| Recurrence | Hourly / Daily / Weekly / Monthly / Yearly |
| Repeat Every N | (e.g., every 2 weeks) |
| Repeat On | (for weekly: Mon, Tue, Wed...) |
| Recurrence End Date | Stop repeating after date |
| Priority | Integer (higher = overrides lower events) |
| Share of Voice (%) | For Ad Campaign events |
| Use Display Timezone? | Yes/No |
| Dayparting | Choose a pre-defined time slot |
| Geo-Location | Enable geofencing for conditional play |
| Is Full Screen? | For overlays |
| Run at CMS time / Player time | Timezone source |

---

### 5.2 Dayparting
**URL**: `/daypart/view`

**Purpose**: Define named time-slot presets (e.g., "Morning: 06:00–09:00").

**Fields**: Name, Start Time, End Time, Days active (Mon-Sun checkboxes)

---

## 📊 SECTION 6 — REPORTING

### 6.1 Proof of Play
**URL**: `/report/proofofplay`

**What it tracks**: Every time a widget/media item plays on a display.

**Filter Options**: Date range, Display, Layout, Media, Widget type

**Export**: CSV, PDF

**Columns**: Date, Display, Layout, Widget, Media Name, Duration Played, Number of Plays

---

### 6.2 Display Statistics
**URL**: `/report/displaystatistics`

**Metrics**: Online time %, Bandwidth used, Last connected

---

### 6.3 Library Usage Report
**URL**: `/report/libraryusage`

**Shows**: Which users/displays are consuming what file storage

---

### 6.4 Audit Trail
**URL**: `/audit/view`

**Tracks**: All entity changes (who changed what, when, with old/new values)

**Filter**: User, Object Type, Date range

---

### 6.5 Log Report
**URL**: `/log/view`

**Shows**: Server-side error/info logs filtered by severity, display, or component

---

## 👥 SECTION 7 — USER & PERMISSIONS MANAGEMENT

### 7.1 Users
**URL**: `/user/view`

**Columns**: ID, Username, Email, User Type, Groups, Library Quota, Home Folder, Last Login, Is Active?

**User Types**:
| Type | Access Level |
|---|---|
| Super Admin | Full access, all features |
| System Admin | Full but no system settings |
| Group Admin | Manage their group's users |
| User | Standard access per permissions |

**Add User Form**:
- Username, Email, Password
- User Type
- Home Folder (folder they see by default)
- Library Quota (MB limit, 0 = unlimited)
- Initial User Group
- Force Password Change on login?

---

### 7.2 User Groups
**URL**: `/group/view`

**Purpose**: Group users for permission management.

**Columns**: ID, Group Name, Description, Is System Group?, Library Quota

**Group permissions**: Per-page, per-feature access control

---

### 7.3 Roles (v4.x)
**URL**: `/role/view`

**Purpose**: Role-based access control (RBAC) layer on top of groups.

**Each Role defines**:
- Pages accessible
- Actions allowed (View/Edit/Delete per module)

---

## ⚙️ SECTION 8 — ADMINISTRATION SETTINGS

**URL**: `/settings`

### Settings Tabs:
| Tab | Key Settings |
|---|---|
| General | CMS Name, Force HTTPS, Google Maps API Key |
| Displays | Default Layout, Collection Interval, Proof of Play defaults |
| Sharing | Allow sharing of layouts/media between users |
| Maintenance | Maintenance IP whitelist, Enable/disable maintenance tasks |
| Network | Proxy server config, HTTPS settings |
| Troubleshooting | Log level (Emergency/Alert/Critical/Error/Warning/Notice/Info/Debug) |
| Regional | Default Timezone, Language/Locale |
| Users | Allow User Registration, Default User Group |
| Transitions | Enable/disable default transition type |
| Metadata | Custom metadata fields for entities |

---

## 🧩 SECTION 9 — MODULES

**URL**: `/module/view`

**Purpose**: Enable/disable which widget types are available in the Layout Designer.

**All Available Modules**:
| Module | Description |
|---|---|
| Image | Static image display |
| Video | MP4/video file playback |
| Audio | Background audio |
| PDF | PDF document viewer |
| Local Video | Play file stored locally on player |
| HLS | HTTP Live Streaming |
| Web Page | Embed external URL (iframe) |
| Embedded | Raw HTML/CSS/JS embed |
| HTML Package | ZIP with index.html |
| Text | Rich text with fonts/colors |
| Ticker | RSS feed or custom text cycling |
| DataSet View | Display DataSet as table |
| DataSet Ticker | DataSet rows cycling as ticker |
| Calendar | iCal feed display |
| Clock | Digital or analogue clock |
| Countdown | Time countdown to event |
| Weather | Forecast widget (OpenWeatherMap API) |
| Twitter Feed | Twitter/X search results |
| Sub-Playlist | Embed another playlist |
| Notifications | CMS notification messages |
| Shell Command | Execute system command |
| Menu Board | Digital menu display (v4.x) |

Each module has:
- Enable/Disable toggle
- Default duration (seconds)
- Module-specific settings

---

## 🎬 SECTION 10 — ADVANCED / SYSTEM

### 10.1 Tasks (CRON Manager)
**URL**: `/task/view`

**Purpose**: Manage background scheduled jobs.

**Default Tasks**:
| Task | Frequency | Description |
|---|---|---|
| Archive Stats | Daily | Archive old playback stats |
| Drop Widgets in Regions | On-demand | Cleanup orphaned widget data |
| Email Notifications | Hourly | Send maintenance alerts |
| Fetch Remote DataSets | Every 5 minutes | Sync external DataSet URLs |
| Generate Proof of Play Summaries | Nightly | Aggregate PoP data |
| Import Layouts | On-trigger | Process imported ZIP layouts |
| Library Cache | Daily | Process thumbnail/preview cache |
| Remove Old Cache | Weekly | Prune file cache |
| Update Display Usage | Hourly | Recalculate bandwidth stats |

---

### 10.2 Player Software
**URL**: `/playersoftware/view`

**Purpose**: Manage downloadable player apps (APK for Android, EXE for Windows).

**Columns**: Version, Type (Android/Windows/Linux), Published?

**Actions**: Upload new version, Publish (makes available for auto-update), Delete

---

### 10.3 Commands
**URL**: `/command/view`

**Purpose**: Define reusable shell commands sent to players remotely.

**Example Commands**: Reboot, Screen On, Screen Off, Volume Up, Volume Down, Clear Cache

**Fields**: Command Name, Code (unique key), Command String (platform-specific)

---

### 10.4 Sessions
**URL**: `/sessions/view`

**Shows**: Active user login sessions, with IP, browser, last activity

**Action**: Force-expire a session

---

### 10.5 Audit Trail
**URL**: `/audit/view`

Full change log for all CMS entities. Tracks: User, Timestamp, Entity Type, Entity ID, Action, Old Value, New Value.

---

### 10.6 Fault Reporting
**URL**: `/fault`

Generates a diagnostic ZIP bundle to send to support. Includes: Server info, PHP config, DB tables summary, error logs.

---

## 🔌 SECTION 11 — API & PLAYER PROTOCOL

The CMS exposes a **RESTful API** used by player clients:

### Player Communication Pattern:
1. **Register** (`POST /display/register`) — Player sends Hardware Key + CMS Key
2. **Check-in / Required Files** (`GET /player/`) — Returns JSON of what files to download
3. **Download Media** (`GET /library/download/{id}`) — Binary file download
4. **Report Stats** (`POST /display/statistics`) — Proof of play logs
5. **Request Screenshot** — CMS can request a player screenshot via command channel

### Authentication: Session tokens or API Key (set per user)

---

## 📐 SECTION 12 — DATA MODELS (Inferred)

### Core Entities:

```
Display
├── id, name, hardware_key, display_profile_id
├── authorized, logged_in, last_accessed
├── latitude, longitude, timezone
├── default_layout_id, tags[], folder_id
└── display_group_ids[]

DisplayGroup
├── id, name, description, is_dynamic
├── criteria (filter rule for dynamic groups)
└── display_ids[] (for static groups)

DisplayProfile
├── id, name, type (android/windows/linux/webos)
└── settings{} (JSON blob of all settings)

Layout
├── id, name, owner_id, status
├── width, height, background_color, background_image_id
├── duration (computed from regions)
├── tags[], folder_id, retired
└── regions[]

Region
├── id, layout_id, name
├── x, y, width, height, z_index
├── duration, loop
└── playlist_id

Playlist
├── id, name, owner_id, tags[]
└── widgets[]

Widget
├── id, playlist_id, module_type, display_order
├── duration, use_duration
├── from_dt, to_dt (expiry)
└── options{} (module-specific JSON)

Media (Library)
├── id, name, owner_id, type
├── file_name, file_size, duration
├── md5, stored_as
├── tags[], folder_id
└── retired, released, expires

DataSet
├── id, name, description, owner_id
├── remote (bool), remote_url, remote_type
├── refresh_rate, last_sync
└── columns[], rows[]

Campaign
├── id, name, type (list/ad), owner_id
├── target_plays (for ad type)
└── layout_ids[] (ordered)

ScheduleEvent
├── id, event_type_id, campaign_id, layout_id
├── display_group_ids[]
├── from_dt, to_dt
├── recurrence_type, recurrence_detail, recurrence_end
├── priority, share_of_voice
└── daypart_id

User
├── id, username, email, password_hash
├── user_type_id, group_ids[]
├── library_quota, home_folder_id
├── retired, last_login
└── api_key

UserGroup
├── id, name, description
├── library_quota
└── user_ids[]

Role
├── id, name, description
└── permissions{} (pages: view/edit/delete per module)

Folder
├── id, parent_id, name
└── permissions{}
```

---

## 🏗️ SECTION 13 — FEASIBILITY & BUILD PLAN

### What to Build (Custom CMS Modules):

| Module | Priority | Complexity | Notes |
|---|---|---|---|
| Auth / User Management | 🔴 Critical | Medium | JWT + RBAC roles |
| Dashboard | 🔴 Critical | Low | Stats aggregation |
| Display Management | 🔴 Critical | Medium | Hardware key auth |
| Layout Builder (Canvas) | 🔴 Critical | **Very High** | Drag-drop canvas |
| Widget System | 🔴 Critical | High | Pluggable modules |
| Media Library | 🔴 Critical | Medium | File upload + S3 |
| Scheduler / Calendar | 🔴 Critical | High | Recurrence engine |
| Playlists | 🟠 High | Medium | Sub-playlist nesting |
| Campaigns | 🟠 High | Medium | SoV algorithm |
| DataSets | 🟠 High | Medium | Custom mini-DB |
| Player API | 🔴 Critical | High | REST endpoint layer |
| Proof of Play Reports | 🟠 High | Medium | Stats ingestion |
| Audit Trail | 🟡 Medium | Low | Event log table |
| CRON/Tasks | 🟡 Medium | Medium | Background workers |
| Display Groups | 🟡 Medium | Low | Static + dynamic |
| Commands | 🟡 Medium | Low | Remote shell |
| Menu Boards | 🟢 Low | Medium | v4 feature |
| Folder System | 🟡 Medium | Medium | Tree hierarchy |

### Recommended Stack:
- **Backend**: PHP (Laravel) — matches existing stack
- **Frontend**: React or Vue.js for the Layout Designer canvas
- **Database**: MySQL (existing via XAMPP)
- **File Storage**: Local (initially), extendable to S3
- **Background Jobs**: Laravel Queue + Scheduler
- **Player API**: REST JSON API with token auth
- **Canvas Engine**: Fabric.js or Konva.js for drag-drop region editor

---

## ✅ CONCLUSION

**It is HIGHLY FEASIBLE** to build a custom CMS with the same capabilities. The system, while complex, is composed of well-defined, independently buildable modules. The most challenging parts are:

1. **Layout Designer** (visual canvas with regions + widget timeline)
2. **Player Communication Protocol** (how screens check-in and download content)
3. **Scheduling Engine** (recurrence, priority resolution, SoV)

Everything else (user management, media library, reporting) is standard CRUD with good UX.
