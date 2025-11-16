import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Provider } from 'urql'
import './index.css'
import App from './App.tsx'
import { graphqlClient } from './lib/graphql-client'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Provider value={graphqlClient}>
      <App />
    </Provider>
  </StrictMode>
)
