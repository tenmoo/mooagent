# MooAgent Frontend

Modern React TypeScript frontend for the MooAgent AI personal assistant.

## Features

- 🎨 Beautiful, modern UI with dark theme
- 💬 Real-time chat interface
- 🔐 Secure authentication
- 📱 Responsive design
- ⚡ Fast and optimized with Vite
- 🎯 Type-safe with TypeScript

## Tech Stack

- **Framework**: React 18
- **Language**: TypeScript
- **Build Tool**: Vite
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Routing**: React Router
- **Deployment**: Vercel

## Setup

### Prerequisites

- Node.js 18+ and npm

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create `.env` file:
```bash
cp .env.example .env
```

3. Edit `.env` and configure API URL:
```env
VITE_API_URL=http://localhost:8000
```

### Running Locally

```bash
npm run dev
```

The app will be available at http://localhost:3000

### Building for Production

```bash
npm run build
```

The build output will be in the `dist` directory.

### Preview Production Build

```bash
npm run preview
```

## Deployment to Vercel

### Prerequisites

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

### Deploy

1. Deploy to production:
```bash
vercel --prod
```

2. Set environment variables in Vercel dashboard:
   - `VITE_API_URL`: Your backend API URL (e.g., https://your-backend.fly.dev)

### Alternative: Deploy via Git

1. Push your code to GitHub
2. Import the project in Vercel dashboard
3. Configure the project:
   - Framework Preset: Vite
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
4. Add environment variable:
   - `VITE_API_URL`: Your backend API URL

## Project Structure

```
frontend/
├── src/
│   ├── pages/          # Page components
│   │   ├── Login.tsx
│   │   ├── Register.tsx
│   │   └── Chat.tsx
│   ├── services/       # API services
│   │   └── api.ts
│   ├── store/          # State management
│   │   ├── authStore.ts
│   │   └── chatStore.ts
│   ├── styles/         # CSS styles
│   │   ├── Auth.css
│   │   └── Chat.css
│   ├── App.tsx         # Main app component
│   ├── main.tsx        # Entry point
│   └── index.css       # Global styles
├── public/             # Static assets
├── index.html          # HTML template
├── package.json        # Dependencies
├── tsconfig.json       # TypeScript config
├── vite.config.ts      # Vite config
└── vercel.json         # Vercel config
```

## Features Overview

### Authentication
- User registration with email and password
- Secure login with JWT tokens
- Protected routes
- Automatic token refresh

### Chat Interface
- Real-time messaging with AI agent
- Message history
- Typing indicators
- Suggested prompts
- Clear chat functionality

### User Experience
- Responsive design for all devices
- Dark theme for comfortable viewing
- Smooth animations and transitions
- Error handling and loading states

## Development

### Code Style

The project uses ESLint for code quality. Run linting:
```bash
npm run lint
```

### Type Checking

TypeScript provides type safety. The build process will fail if there are type errors.

## Environment Variables

- `VITE_API_URL`: Backend API URL (required)

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

MIT
