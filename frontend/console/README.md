# Console - Internal Admin Dashboard

A React-based admin console for managing the Django GCP boilerplate application.

## Tech Stack

- **Vite 7.2** - Fast build tool and dev server
- **React 19.2** - UI library with latest features
- **TypeScript 5.9** - Type safety
- **Tailwind CSS 4.1** - Utility-first CSS framework
- **shadcn/ui** - High-quality component library
- **urql 5.0** - Lightweight GraphQL client
- **React Router 7.9** - Client-side routing
- **WorkOS** - Authentication and user management

## Getting Started

### Prerequisites

- Node.js 24 (LTS) and npm
- Django backend running on `http://localhost:8000`
- WorkOS account with client ID configured

### Installation

```bash
cd frontend/console
npm install
```

### Environment Variables

Create a `.env` file in the `frontend/console` directory:

```bash
VITE_GRAPHQL_URL=http://localhost:8000/graphql/
VITE_WORKOS_CLIENT_ID=your_workos_client_id
VITE_WORKOS_REDIRECT_URI=http://localhost:3000/auth/callback
```

See `.env.example` for reference.

### Development

Start the development server:

```bash
npm run dev
```

The app will be available at `http://localhost:5173` (Vite default port).

### Building for Production

Build the static files:

```bash
npm run build
```

The output will be in the `dist/` directory, ready to be deployed to a GCS bucket or any static hosting service.

Preview the production build locally:

```bash
npm run preview
```

## Project Structure

```
src/
├── components/          # Reusable React components
│   └── ProtectedRoute.tsx
├── pages/              # Page components
│   ├── Login.tsx
│   ├── AuthCallback.tsx
│   └── Dashboard.tsx
├── lib/                # Utilities and configurations
│   ├── graphql-client.ts
│   ├── auth.ts
│   └── utils.ts
├── graphql/            # GraphQL queries and mutations
│   └── mutations.ts
├── App.tsx             # Main app component with routing
├── main.tsx            # Entry point
└── index.css           # Global styles
```

## Authentication Flow

1. User visits the app → redirected to `/login`
2. `/login` redirects to WorkOS OAuth login page
3. After successful login, WorkOS redirects to `/auth/callback?code=...`
4. The callback page exchanges the code for a token via GraphQL mutation
5. Token is stored in localStorage
6. User is redirected to `/dashboard`

All subsequent GraphQL requests include the token in the Authorization header.

## Adding shadcn/ui Components

This project uses shadcn/ui components. To add a new component:

```bash
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add input
# etc.
```

Components will be added to `src/components/ui/`.

## GraphQL Code Generation

This project uses GraphQL Code Generator to automatically generate TypeScript types from the backend GraphQL schema.

### Initial Setup

1. Make sure the Django backend is running on `http://localhost:8000`

2. Fetch the GraphQL schema from the backend:

```bash
npm run genschema
```

This will download the schema and save it to `src/gql/schema.graphql`.

3. Generate TypeScript types from GraphQL operations:

```bash
npm run gentypes
```

This will scan all `.ts` and `.tsx` files for GraphQL queries/mutations and generate typed hooks in `src/__generated__/`.

### Workflow

**After adding or modifying GraphQL queries/mutations:**

```bash
npm run gentypes
```

**After backend schema changes:**

```bash
npm run codegen  # Runs both genschema and gentypes
```

### Available Scripts

- `npm run genschema` - Fetch schema from backend → `src/gql/schema.graphql`
- `npm run gentypes` - Generate TypeScript types from queries/mutations → `src/__generated__/`
- `npm run codegen` - Run both commands in sequence

### Using Generated Types

After running codegen, you can import and use typed hooks:

```tsx
import { graphql } from '@/\_\_generated\_\_'

// Define your query
const MyQuery = graphql(`
  query GetUser($id: ID!) {
    user(id: $id) {
      id
      email
      firstName
      lastName
    }
  }
`)

// Use in component with full type safety
function UserProfile({ userId }: { userId: string }) {
  const [result] = useQuery({ query: MyQuery, variables: { id: userId } })

  if (result.fetching) return <div>Loading...</div>
  if (result.error) return <div>Error: {result.error.message}</div>

  return <div>{result.data?.user?.email}</div>
}
```

All types are automatically inferred, providing full IntelliSense and type checking!

## Routing

Routes are configured in `src/App.tsx`:

- `/` - Redirects to `/dashboard`
- `/login` - Login page (redirects to WorkOS)
- `/auth/callback` - OAuth callback handler
- `/dashboard` - Main dashboard (protected)

All protected routes use the `<ProtectedRoute>` wrapper which checks for authentication.

## Deployment

The console is designed to be deployed as a static site.

### Option 1: Google App Engine (Recommended)

**Prerequisites**:

- Google Cloud SDK installed
- Authenticated: `gcloud auth login`
- Project set: `gcloud config set project YOUR_PROJECT_ID`

**Setup Production Environment**:

1. Create `.env.production.local` with your production settings:

```bash
cp .env.production .env.production.local

# Edit .env.production.local with your values:
VITE_GRAPHQL_URL=https://your-backend-service.run.app/graphql/
VITE_WORKOS_CLIENT_ID=your_production_workos_client_id
VITE_WORKOS_REDIRECT_URI=https://console-dot-YOUR-PROJECT-ID.uc.r.appspot.com/auth/callback
```

**Note**: Replace `YOUR-PROJECT-ID` with your actual GCP project ID.

2. **Configure WorkOS Redirect URI**:
   - Go to WorkOS Dashboard
   - Add production redirect URI: `https://console-dot-YOUR-PROJECT-ID.uc.r.appspot.com/auth/callback`

3. **Deploy**:

```bash
npm run deploy
```

This will:

- Build the app with production environment variables
- Deploy to Google App Engine as the `console` service
- Serve at: `https://console-dot-YOUR-PROJECT-ID.uc.r.appspot.com`

**Manual deployment**:

```bash
npm run build:prod
gcloud app deploy app.yaml
```

**Update `app.yaml` if needed**:
The `app.yaml` file is pre-configured with:

- Static file serving
- Client-side routing support (SPA)
- Cache headers (assets cached for 1 year, HTML no-cache)
- All favicon files configured

### Option 2: Google Cloud Storage (Static Hosting)

1. Build the app:

   ```bash
   npm run build:prod
   ```

2. Upload to GCS bucket:

   ```bash
   gsutil -m rsync -r -d dist/ gs://your-bucket-name/
   ```

3. Configure bucket for static website hosting:

   ```bash
   gsutil web set -m index.html -e index.html gs://your-bucket-name
   ```

4. Make bucket public:
   ```bash
   gsutil iam ch allUsers:objectViewer gs://your-bucket-name
   ```

### Option 3: Other Static Hosts

The `dist/` folder can be deployed to:

- **Vercel**: `vercel --prod`
- **Netlify**: `netlify deploy --prod`
- **Cloudflare Pages**: via Git integration
- **GitHub Pages**: via GitHub Actions
- **AWS S3 + CloudFront**
- **Azure Static Web Apps**

## Scripts

### Development

- `npm run dev` - Start development server

### Build

- `npm run build` - Build for production (development mode)
- `npm run build:prod` - Build for production with production env vars
- `npm run preview` - Preview production build

### Deployment

- `npm run deploy` - Build and deploy to Google App Engine

### GraphQL Code Generation

- `npm run genschema` - Fetch GraphQL schema from backend
- `npm run gentypes` - Generate TypeScript types from GraphQL operations
- `npm run codegen` - Run both genschema and gentypes

### Code Quality

- `npm run lint` - Run ESLint and TypeScript checks
- `npm run lint:fix` - Auto-fix ESLint issues and run TypeScript checks
- `npm run format` - Format code with Prettier
- `npm run style` - Format and fix all code issues (runs format + lint:fix)

## License

Same as the parent project.
