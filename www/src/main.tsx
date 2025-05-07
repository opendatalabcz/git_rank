import { createRoot } from 'react-dom/client'
import './main.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import App from './App.tsx'
import React from 'react'
import Footer from './components/Footer.tsx'

createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
    <Footer />
  </React.StrictMode>
)
