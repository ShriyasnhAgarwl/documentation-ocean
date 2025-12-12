# Roboi - Implementation Guide

## Overview
This guide provides step-by-step instructions for implementing the Nayara Admin dashboard following the established architecture.

## Phase 1: Project Setup ✅

### 1.1 Initialize Project Structure
```bash
# Make setup script executable
chmod +x setup-structure.sh

# Run setup script
./setup-structure.sh

# Install dependencies
npm install
```

### 1.2 Environment Configuration
```bash
# Copy environment template
cp .env.example .env.local

# Add your Mapbox token
# NEXT_PUBLIC_MAPBOX_TOKEN=your_token_here
```

### 1.3 Verify Setup
```bash
# Run development server
npm run dev

# Should start on http://localhost:3000
```

## Phase 2: Core Infrastructure

### 2.1 Create Base Layout Components

#### Priority Order:
1. **DashboardLayout** (`src/components/layout/DashboardLayout/`)
   - Main layout wrapper
   - Includes Sidebar and Header
   - Handles responsive behavior

2. **Sidebar** (`src/components/layout/Sidebar/`)
   - Navigation menu
   - Logo and branding
   - Active state management
   - Collapsible on mobile

3. **Header** (`src/components/layout/Header/`)
   - User profile
   - Notifications
   - Theme toggle
   - Breadcrumbs

### 2.2 Create Base UI Components

#### Priority Order:
1. **Button** - Most used component
2. **Card** - Container for widgets
3. **Input** - Form inputs
4. **Modal** - Dialogs and popups
5. **Dropdown** - Select menus
6. **Table** - Data display
7. **Tabs** - Content organization
8. **Badge** - Status indicators
9. **Skeleton** - Loading states

### 2.3 Set Up State Management

#### Zustand Store Structure:
```javascript
// src/store/slices/authSlice.js
// src/store/slices/filtersSlice.js
// src/store/slices/uiSlice.js
// src/store/index.js
```

### 2.4 Set Up API Client

#### Axios Configuration:
```javascript
// src/lib/axios.js
// - Base URL configuration
// - Request/response interceptors
// - Error handling
// - Token management
```

### 2.5 Set Up React Query

```javascript
// src/lib/queryClient.js
// - Query client configuration
// - Default options
// - Cache settings
```

## Phase 3: Visualization Components

### 3.1 Chart Components (ECharts)

#### Implementation Order:
1. **BaseChart** - Wrapper component
   - Common configuration
   - Responsive handling
   - Theme support
   - Loading states

2. **LineChart** - For trends
3. **BarChart** - For comparisons
4. **PieChart** - For distributions
5. **GaugeChart** - For metrics
6. **HeatMap** - For intensity
7. **TreeMap** - For hierarchical data
8. **SankeyChart** - For flow data

#### Example BaseChart Structure:
```javascript
// src/components/charts/BaseChart/BaseChart.js
import ReactECharts from 'echarts-for-react';
import { CHART_CONFIG } from '@/config/chart.config';

export default function BaseChart({ option, loading, height = '400px' }) {
  // Implementation
}
```

### 3.2 Map Components (Mapbox)

#### Implementation Order:
1. **BaseMap** - Wrapper component
   - Map initialization
   - Controls setup
   - Event handling
   - Responsive behavior

2. **StateMap** - State-level visualization
3. **CityMap** - City-level visualization
4. **HeatMapOverlay** - Density visualization
5. **MarkerCluster** - Multiple markers

#### Example BaseMap Structure:
```javascript
// src/components/maps/BaseMap/BaseMap.js
import Map, { NavigationControl, GeolocateControl } from 'react-map-gl';
import { MAP_CONFIG } from '@/config/map.config';

export default function BaseMap({ children, ...props }) {
  // Implementation
}
```

### 3.3 Widget Components

#### Implementation Order:
1. **StatsCard** - Metric display
2. **TrendCard** - Metric with trend
3. **AlertCard** - Alert display
4. **ActivityFeed** - Recent activities

## Phase 4: Feature Implementation

### 4.1 HQ Overview Page

#### Components to Build:
1. **PumpStatusGrid** - Grid of pump statuses
2. **RealtimeMetrics** - Live metrics cards
3. **AlertsPanel** - Recent alerts
4. **GeographicHeatMap** - Map with heat overlay
5. **PumpDistribution** - Pie chart
6. **AlertTimeline** - Line chart

#### Data Flow:
```
API → React Query → Components → UI
  ↓
WebSocket → Real-time Updates
```

#### Implementation Steps:
1. Create page layout (`src/app/(dashboard)/hq-overview/page.js`)
2. Build feature components (`src/components/features/hq-overview/`)
3. Create API service (`src/services/api/analytics.js`)
4. Set up React Query hooks (`src/hooks/useAnalytics.js`)
5. Implement WebSocket connection (`src/services/websocket/realtimeService.js`)

### 4.2 State-wise Analytics Page

#### Components to Build:
1. **StateSelector** - Dropdown/map selector
2. **StateOverviewMap** - Map with markers
3. **PumpDistributionChart** - Bar chart
4. **PerformanceTrends** - Line chart
5. **AlertDistribution** - Heat map
6. **CityComparisonTable** - Data table

#### Implementation Steps:
1. Create page layout
2. Build feature components
3. Implement state selection logic
4. Add filtering capabilities
5. Implement export functionality

### 4.3 City-wise Analytics Page

#### Components to Build:
1. **CitySelector** - Cascading selector
2. **CityMap** - Map with pump locations
3. **PumpStatusGrid** - Individual pump grid
4. **TrafficPatterns** - Heat map
5. **VehicleCountTrends** - Area chart
6. **PerformanceMetrics** - Gauge charts

#### Implementation Steps:
1. Create page layout
2. Build feature components
3. Implement cascading filters
4. Add drill-down capability
5. Implement export functionality

### 4.4 ANPR Vehicles Page

#### Components to Build:
1. **VehicleGrid** - Grid/list view
2. **VehicleFilters** - Advanced filters
3. **VehicleSearch** - Search with autocomplete
4. **QuickStats** - Summary cards
5. **BulkExport** - Export functionality

#### Implementation Steps:
1. Create page layout
2. Build feature components
3. Implement search and filters
4. Add pagination/infinite scroll
5. Implement export functionality

### 4.5 Vehicle Profile Page

#### Components to Build:
1. **VehicleInfo** - Basic information
2. **VehicleTimeline** - Visit timeline
3. **VisitHistory** - Table of visits
4. **VehicleImages** - Image gallery
5. **VehicleReports** - Reports section
6. **ReportDownload** - Download options

#### Implementation Steps:
1. Create dynamic page (`src/app/(dashboard)/vehicle-profile/[vehicleId]/page.js`)
2. Build feature components
3. Implement data fetching
4. Add report generation
5. Implement download functionality

## Phase 5: Common Components

### 5.1 DataTable Component

#### Features:
- Sorting
- Filtering
- Pagination
- Row selection
- Custom columns
- Export functionality

### 5.2 SearchBar Component

#### Features:
- Debounced search
- Autocomplete
- Recent searches
- Clear functionality

### 5.3 FilterPanel Component

#### Features:
- Multiple filter types
- Date range picker
- Multi-select
- Save filter presets
- Clear all filters

### 5.4 DateRangePicker Component

#### Features:
- Preset ranges
- Custom range
- Calendar view
- Validation

### 5.5 ExportButton Component

#### Features:
- Multiple formats (PDF, Excel, CSV, PNG)
- Progress indicator
- Error handling
- Download management

## Phase 6: Services & Hooks

### 6.1 API Services

#### Structure:
```javascript
// src/services/api/analytics.js
export const analyticsService = {
  getHQOverview: () => axios.get('/analytics/hq-overview'),
  getStateWise: (stateId) => axios.get(`/analytics/state/${stateId}`),
  getCityWise: (cityId) => axios.get(`/analytics/city/${cityId}`),
};
```

### 6.2 Custom Hooks

#### Essential Hooks:
1. **useAuth** - Authentication
2. **useAnalytics** - Analytics data
3. **useVehicles** - Vehicle data
4. **useReports** - Report generation
5. **useFilters** - Filter management
6. **useExport** - Export functionality
7. **useWebSocket** - Real-time updates
8. **useDebounce** - Debounced values

## Phase 7: Styling & Theming

### 7.1 Global Styles

```css
/* src/styles/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom global styles */
```

### 7.2 Theme Configuration

```javascript
// src/components/providers/ThemeProvider.js
// - Light/dark mode
// - Theme persistence
// - System preference detection
```

### 7.3 Chart Theming

```css
/* src/styles/charts.css */
/* Chart-specific styles */
```

## Phase 8: Testing & Optimization

### 8.1 Testing

#### Test Coverage:
- Unit tests for utilities
- Component tests
- Integration tests
- E2E tests (critical flows)

### 8.2 Performance Optimization

#### Checklist:
- [ ] Code splitting implemented
- [ ] Lazy loading for charts
- [ ] Image optimization
- [ ] Memoization applied
- [ ] Virtual scrolling for lists
- [ ] Debounced inputs
- [ ] React Query caching configured

### 8.3 Accessibility

#### Checklist:
- [ ] ARIA labels added
- [ ] Keyboard navigation
- [ ] Focus management
- [ ] Color contrast verified
- [ ] Screen reader tested

## Phase 9: Deployment

### 9.1 Build Configuration

```bash
# Build for production
npm run build

# Test production build locally
npm start
```

### 9.2 Environment Variables

Ensure all production environment variables are set:
- API URLs
- Mapbox token
- Analytics ID
- Feature flags

### 9.3 Deployment Checklist

- [ ] Environment variables configured
- [ ] Build successful
- [ ] No console errors
- [ ] Performance tested
- [ ] Security headers configured
- [ ] SSL certificate installed
- [ ] CDN configured
- [ ] Monitoring set up

## Development Best Practices

### Code Organization
1. One component per file
2. Co-locate related files
3. Use index.js for exports
4. Keep components small (<200 lines)

### Naming Conventions
1. PascalCase for components
2. camelCase for functions/variables
3. UPPER_CASE for constants
4. Descriptive names

### Component Structure
```javascript
// 1. Imports
import React from 'react';

// 2. Component definition
export default function ComponentName({ prop1, prop2 }) {
  // 3. Hooks
  const [state, setState] = useState();
  
  // 4. Effects
  useEffect(() => {}, []);
  
  // 5. Handlers
  const handleClick = () => {};
  
  // 6. Render
  return <div>...</div>;
}
```

### Git Workflow
1. Create feature branch
2. Make changes
3. Run linting: `npm run lint:fix`
4. Run tests: `npm test`
5. Commit with meaningful message
6. Create pull request

## Troubleshooting

### Common Issues

#### 1. Mapbox not loading
- Check token in `.env.local`
- Verify token is valid
- Check network requests

#### 2. Charts not rendering
- Verify ECharts installed
- Check console for errors
- Ensure data format is correct

#### 3. WebSocket connection failing
- Check WebSocket URL
- Verify backend is running
- Check CORS configuration

#### 4. Build errors
- Clear `.next` folder
- Delete `node_modules` and reinstall
- Check for TypeScript errors

## Next Steps

1. **Phase 1**: Set up project ✅
2. **Phase 2**: Build core infrastructure
3. **Phase 3**: Implement visualizations
4. **Phase 4**: Build features
5. **Phase 5**: Add common components
6. **Phase 6**: Create services & hooks
7. **Phase 7**: Apply styling & theming
8. **Phase 8**: Test & optimize
9. **Phase 9**: Deploy

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [ECharts Documentation](https://echarts.apache.org/en/index.html)
- [Mapbox GL JS Documentation](https://docs.mapbox.com/mapbox-gl-js/)
- [React Query Documentation](https://tanstack.com/query/latest)
- [Zustand Documentation](https://github.com/pmndrs/zustand)

---

**Last Updated**: 2025-12-12  
**Version**: 1.0.0
