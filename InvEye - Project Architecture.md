# InvEye - Project Architecture

## Project Overview
**inveye - Real-time Analytics Dashboard**  
Video Analytics · 7,000+ Pumps · Real-time AI

A production-grade, highly scalable Next.js application for managing and visualizing video analytics data across 7,000+ fuel pumps with real-time AI capabilities. Built with an optimized tech stack for maximum performance and maintainability.

## Tech Stack

### Core Framework
- **Next.js 14+** (App Router) - React framework with server-side rendering
- **JavaScript** - Primary programming language
- **Tailwind CSS** - Utility-first CSS framework

### Visualization Libraries
- **Apache ECharts** - Primary charting library (recommended for production)
  - Pros: Superior performance, extensive chart types, excellent documentation
  - Free, open-source, production-ready
  - Better for large datasets (7,000+ pumps)
  - Handles: Line, Bar, Pie, Gauge, Heatmap, Treemap, Sankey charts
- **Mapbox GL JS** - Interactive maps and geospatial visualization
  - Free tier available (50,000 loads/month)
  - Superior performance and customization
  - WebGL-based rendering

### State Management
- **TanStack Query (React Query)** - Server state management, caching, and data fetching
  - Handles all API data, automatic caching, background updates
  - Optimistic updates and request deduplication
- **Zustand** - Client state management
  - Lightweight state for UI state, filters, user preferences
  - Simple API, no boilerplate

### Data Fetching
- **Axios** - HTTP client with interceptors
- **SWR** (alternative) - For real-time data updates

### UI Components
- **Radix UI** - Accessible, unstyled primitive components
  - Production-ready, comprehensive component library
  - Built-in accessibility (ARIA)
  - Highly customizable
- **React Icons** - Comprehensive icon library

### Utilities
- **date-fns** - Date manipulation and formatting
- **clsx** - Conditional className management
- **react-hot-toast** - Toast notifications

### Export & Reports
- **jsPDF** - PDF generation
- **jspdf-autotable** - PDF table formatting
- **xlsx** - Excel file generation

### Development Tools
- **ESLint** - Code linting
- **Prettier** - Code formatting
- **Husky** - Git hooks
- **lint-staged** - Run linters on staged files

## Project Structure

```
inveye-web/
├── .github/                      # GitHub workflows and templates
├── .husky/                       # Git hooks
├── public/                       # Static assets
│   ├── images/
│   ├── icons/
│   └── fonts/
├── src/
│   ├── app/                      # Next.js App Router
│   │   ├── (auth)/              # Auth route group
│   │   │   ├── login/
│   │   │   └── layout.js
│   │   ├── (dashboard)/         # Dashboard route group
│   │   │   ├── layout.js        # Dashboard layout with sidebar
│   │   │   ├── hq-overview/     # HQ Overview page
│   │   │   ├── state-wise/      # State-wise analytics
│   │   │   ├── city-wise/       # City-wise analytics
│   │   │   ├── anpr-vehicles/   # ANPR captured vehicles
│   │   │   └── vehicle-profile/ # Vehicle profile & reports
│   │   │       └── [vehicleId]/
│   │   ├── api/                 # API routes
│   │   │   ├── analytics/
│   │   │   ├── vehicles/
│   │   │   └── reports/
│   │   ├── layout.js            # Root layout
│   │   ├── page.js              # Home page (redirects to dashboard)
│   │   ├── error.js             # Error boundary
│   │   ├── loading.js           # Loading UI
│   │   └── not-found.js         # 404 page
│   ├── components/              # Reusable components
│   │   ├── ui/                  # Base UI components
│   │   │   ├── Button/
│   │   │   ├── Card/
│   │   │   ├── Modal/
│   │   │   ├── Dropdown/
│   │   │   ├── Input/
│   │   │   ├── Table/
│   │   │   ├── Tabs/
│   │   │   ├── Badge/
│   │   │   ├── Skeleton/
│   │   │   └── index.js
│   │   ├── layout/              # Layout components
│   │   │   ├── Sidebar/
│   │   │   ├── Header/
│   │   │   ├── Footer/
│   │   │   └── DashboardLayout/
│   │   ├── charts/              # Chart components
│   │   │   ├── BaseChart/       # ECharts wrapper
│   │   │   ├── LineChart/
│   │   │   ├── BarChart/
│   │   │   ├── PieChart/
│   │   │   ├── HeatMap/
│   │   │   ├── GaugeChart/
│   │   │   ├── TreeMap/
│   │   │   ├── SankeyChart/
│   │   │   └── index.js
│   │   ├── maps/                # Map components
│   │   │   ├── BaseMap/         # Mapbox wrapper
│   │   │   ├── StateMap/
│   │   │   ├── CityMap/
│   │   │   ├── HeatMapOverlay/
│   │   │   ├── MarkerCluster/
│   │   │   └── index.js
│   │   ├── widgets/             # Dashboard widgets
│   │   │   ├── StatsCard/
│   │   │   ├── TrendCard/
│   │   │   ├── AlertCard/
│   │   │   ├── ActivityFeed/
│   │   │   └── index.js
│   │   ├── features/            # Feature-specific components
│   │   │   ├── hq-overview/
│   │   │   │   ├── PumpStatusGrid/
│   │   │   │   ├── RealtimeMetrics/
│   │   │   │   ├── AlertsPanel/
│   │   │   │   └── index.js
│   │   │   ├── state-wise/
│   │   │   │   ├── StateSelector/
│   │   │   │   ├── StateAnalytics/
│   │   │   │   └── index.js
│   │   │   ├── city-wise/
│   │   │   │   ├── CitySelector/
│   │   │   │   ├── CityAnalytics/
│   │   │   │   └── index.js
│   │   │   ├── anpr-vehicles/
│   │   │   │   ├── VehicleGrid/
│   │   │   │   ├── VehicleFilters/
│   │   │   │   ├── VehicleSearch/
│   │   │   │   └── index.js
│   │   │   └── vehicle-profile/
│   │   │       ├── VehicleInfo/
│   │   │       ├── VehicleTimeline/
│   │   │       ├── VehicleReports/
│   │   │       ├── ReportDownload/
│   │   │       └── index.js
│   │   └── common/              # Common components
│   │       ├── DataTable/
│   │       ├── SearchBar/
│   │       ├── FilterPanel/
│   │       ├── DateRangePicker/
│   │       ├── ExportButton/
│   │       ├── Pagination/
│   │       └── index.js
│   ├── providers/               # Context providers (app-level)
│   │   ├── ThemeProvider.js
│   │   ├── AuthProvider.js
│   │   └── QueryProvider.js
│   ├── lib/                     # Library configurations
│   │   ├── axios.js             # Axios instance
│   │   ├── echarts.js           # ECharts configuration
│   │   ├── mapbox.js            # Mapbox configuration
│   │   ├── queryClient.js       # React Query client
│   │   └── utils.js             # Utility functions
│   ├── hooks/                   # Custom React hooks
│   │   ├── useAuth.js
│   │   ├── useAnalytics.js
│   │   ├── useVehicles.js
│   │   ├── useReports.js
│   │   ├── useFilters.js
│   │   ├── useExport.js
│   │   ├── useWebSocket.js      # Real-time updates
│   │   └── useDebounce.js
│   ├── services/                # API services
│   │   ├── api/
│   │   │   ├── analytics.js
│   │   │   ├── vehicles.js
│   │   │   ├── reports.js
│   │   │   ├── auth.js
│   │   │   └── index.js
│   │   └── websocket/
│   │       └── realtimeService.js
│   ├── store/                   # State management
│   │   ├── slices/
│   │   │   ├── authSlice.js
│   │   │   ├── filtersSlice.js
│   │   │   ├── uiSlice.js
│   │   │   └── index.js
│   │   └── index.js
│   ├── styles/                  # Global styles
│   │   ├── globals.css          # Global CSS + Tailwind
│   │   ├── themes/
│   │   │   ├── light.css
│   │   │   └── dark.css
│   │   └── charts.css           # Chart-specific styles
│   ├── utils/                   # Utility functions
│   │   ├── formatters.js        # Data formatters
│   │   ├── validators.js        # Validation functions
│   │   ├── constants.js         # App constants
│   │   ├── chartHelpers.js      # Chart configuration helpers
│   │   ├── mapHelpers.js        # Map utilities
│   │   ├── exportHelpers.js     # Export/download utilities
│   │   └── index.js
│   ├── config/                  # Configuration files
│   │   ├── app.config.js        # App configuration
│   │   ├── chart.config.js      # Default chart configs
│   │   ├── map.config.js        # Map configurations
│   │   └── routes.config.js     # Route definitions
│   └── types/                   # Type definitions (JSDoc)
│       ├── analytics.js
│       ├── vehicle.js
│       └── index.js
├── src/
│   └── middleware.js            # Next.js middleware (auth, redirects)
├── .env.local                   # Environment variables
├── .env.example                 # Example environment variables
├── .eslintrc.json              # ESLint configuration
├── .prettierrc                 # Prettier configuration
├── next.config.js              # Next.js configuration
├── tailwind.config.js          # Tailwind configuration
├── postcss.config.js           # PostCSS configuration
├── jsconfig.json               # JavaScript configuration
├── package.json
└── README.md

```

## Key Architecture Decisions

### 1. Next.js App Router
- Using App Router for better performance and modern React features
- Route groups for logical separation (auth, dashboard)
- Server components by default for better performance
- Client components only when needed (interactivity, hooks)

### 2. Component Architecture
- **Atomic Design Pattern**: UI components → Widgets → Features → Pages
- **Composition over Configuration**: Small, composable components
- **Single Responsibility**: Each component has one clear purpose
- **Reusability**: Shared components in `/components/ui` and `/components/common`

### 3. Data Flow
```
API/WebSocket → Services → React Query → Components → UI
                              ↓
                          Zustand Store (global state)
```

### 4. Visualization Strategy
- **ECharts** for all standard charts (line, bar, pie, gauge, heatmap, treemap, sankey)
  - Production-ready with excellent performance
  - Handles large datasets efficiently (7,000+ pumps)
  - Comprehensive chart types cover 95%+ of needs
- **Mapbox** for all map-based visualizations
  - Geographic heatmaps, markers, clusters
  - State and city-level visualizations
  - Route and path visualization
- **Two-library approach**: Lean stack, no redundancy
- Lazy loading for chart components
- Memoization for chart configurations
- Responsive and theme-aware

### 5. State Management Strategy
- **React Query**: Server state, caching, background updates
- **Zustand**: Client state (filters, UI state, user preferences)
- **URL State**: For shareable filters and views
- **Local State**: Component-specific state

### 6. Performance Optimizations
- Code splitting by route
- Dynamic imports for heavy components
- Image optimization with Next.js Image
- Memoization of expensive calculations
- Virtual scrolling for large lists
- Debounced search and filters
- Progressive loading for dashboards

### 7. Real-time Updates
- WebSocket connection for live data
- Fallback to polling if WebSocket fails
- Optimistic updates for better UX
- Background data synchronization

## Page Specifications

### 1. HQ Overview (`/hq-overview`)
**Purpose**: High-level overview of all 7,000+ pumps

**Components**:
- Real-time metrics cards (total pumps, active, alerts, incidents)
- Geographic heat map (Mapbox)
- Pump status distribution (pie chart)
- Alert timeline (line chart)
- Recent activity feed
- Top performing states/cities

**Data Updates**: Real-time via WebSocket

### 2. State-wise Analytics (`/state-wise`)
**Purpose**: State-level drill-down analytics

**Components**:
- State selector (dropdown/map)
- State overview map (Mapbox with markers)
- Pump distribution by city (bar chart)
- Performance trends (line chart)
- Alert distribution (heat map)
- City comparison table
- Export functionality

**Filters**: Date range, pump status, alert types

### 3. City-wise Analytics (`/city-wise`)
**Purpose**: City-level detailed analytics

**Components**:
- City selector (cascading: state → city)
- City map with pump locations (Mapbox)
- Individual pump status grid
- Traffic patterns (heat map)
- Vehicle count trends (area chart)
- Performance metrics (gauge charts)
- Export functionality

**Filters**: Date range, pump IDs, vehicle types

### 4. ANPR Captured Vehicles (`/anpr-vehicles`)
**Purpose**: View all captured vehicles

**Components**:
- Advanced search and filters
- Vehicle grid/list view (with thumbnails)
- Pagination/infinite scroll
- Quick stats (total vehicles, unique, flagged)
- Filter panel (date, location, vehicle type, number plate)
- Bulk export functionality

**Features**:
- Click to view vehicle profile
- Sort by various parameters
- Save filter presets

### 5. Vehicle Profile (`/vehicle-profile/[vehicleId]`)
**Purpose**: Detailed vehicle information and reports

**Components**:
- Vehicle information card
- Capture timeline (map + timeline chart)
- All pump visits (table)
- Vehicle images gallery
- Reports section
- Download options (PDF, Excel, CSV)

**Sub-sections**:
- Basic info (number plate, type, first/last seen)
- Visit history with map
- Analytics (frequency, patterns)
- Flagged incidents
- Generated reports

## Shared Components Library

### Charts (Reusable - ECharts)
1. **LineChart** - Trends over time
2. **BarChart** - Comparisons and distributions
3. **PieChart** - Percentage distributions
4. **GaugeChart** - Performance metrics and KPIs
5. **HeatMap** - Intensity and density visualization
6. **TreeMap** - Hierarchical data visualization
7. **SankeyChart** - Flow and process visualization

### Maps (Reusable - Mapbox)
1. **BaseMap** - Mapbox wrapper component
2. **MarkerCluster** - Multiple location clustering
3. **HeatMapOverlay** - Geographic density visualization
4. **RouteMap** - Vehicle paths and routes

### Widgets (Reusable)
1. **StatsCard** - Metric display
2. **TrendCard** - Metric with trend
3. **AlertCard** - Alert/notification

### Common (Reusable)
1. **DataTable** - Sortable, filterable table
2. **SearchBar** - Search with autocomplete
3. **FilterPanel** - Advanced filters
4. **DateRangePicker** - Date selection
5. **ExportButton** - Download functionality
6. **Pagination** - Page navigation

## Data Export Strategy

### Export Formats
- **PDF**: Reports with charts and tables
- **Excel**: Raw data with formatting
- **CSV**: Simple data export
- **PNG/SVG**: Chart images

### Implementation
- Client-side generation for small datasets
- Server-side generation for large datasets
- Background jobs for bulk exports
- Email delivery for large reports

## Security Considerations

1. **Authentication**: JWT-based auth
2. **Authorization**: Role-based access control
3. **API Security**: Rate limiting, CORS
4. **Data Validation**: Input sanitization
5. **XSS Protection**: Content Security Policy
6. **HTTPS Only**: Force secure connections

## Scalability Considerations

1. **Code Splitting**: Route-based and component-based
2. **Lazy Loading**: Charts and heavy components
3. **Caching**: React Query for API responses
4. **CDN**: Static assets delivery
5. **Image Optimization**: Next.js Image component
6. **Database Indexing**: Backend optimization
7. **Pagination**: For large datasets
8. **Virtual Scrolling**: For long lists

## Development Workflow

1. **Branch Strategy**: GitFlow (main, develop, feature/*, hotfix/*)
2. **Code Review**: Required for all PRs
3. **Testing**: Unit tests (Jest), E2E tests (Playwright)
4. **CI/CD**: Automated testing and deployment
5. **Documentation**: JSDoc for all functions

## Environment Variables

```env
# App
NEXT_PUBLIC_APP_URL=
NEXT_PUBLIC_API_URL=
NEXT_PUBLIC_WS_URL=

# Mapbox
NEXT_PUBLIC_MAPBOX_TOKEN=

# Analytics
NEXT_PUBLIC_ANALYTICS_ID=

# Feature Flags
NEXT_PUBLIC_ENABLE_REALTIME=true
NEXT_PUBLIC_ENABLE_EXPORT=true
```

## Getting Started

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linting
npm run lint

# Run tests
npm test
```

## Best Practices

1. **Component Naming**: PascalCase for components, camelCase for utilities
2. **File Organization**: One component per file
3. **Props Validation**: Use PropTypes or JSDoc
4. **Error Handling**: Comprehensive error boundaries
5. **Loading States**: Skeleton screens for better UX
6. **Accessibility**: ARIA labels, keyboard navigation
7. **Performance**: Memoization, lazy loading
8. **Code Quality**: ESLint, Prettier, Husky

## Monitoring & Analytics

1. **Error Tracking**: Sentry or similar
2. **Performance Monitoring**: Web Vitals
3. **User Analytics**: Google Analytics or Mixpanel
4. **Real-time Monitoring**: Dashboard health checks

---

**Last Updated**: 2025-12-12  
**Version**: 1.0.0  
**Maintained By**: Development Team
