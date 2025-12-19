import React from 'react'
import LiquidEther from '../LiquidEther.jsx'
import '../LiquidEther.css'

export default function App() {
  return (
    <div style={styles.wrapper}>
      {/* ФОН */}
      <LiquidEther
        mouseForce={25}
        cursorSize={120}
        resolution={0.6}
        colors={['#5B6CFF', '#FF7AD9', '#9F8CFF']}
        autoDemo={true}
        autoSpeed={0.6}
        autoIntensity={2.4}
      />

      {/* ЦЕНТРАЛЬНАЯ КАРТОЧКА */}
      <div style={styles.card}>
        <h1 style={styles.title}>Телефонный справочник</h1>
        <p style={styles.subtitle}>
          Веб-приложение для хранения и поиска абонентов
        </p>

        <a
          href="/subscribers.html"
          className="cta-button"
          style={styles.button}
          onMouseMove={(e) => {
            const rect = e.currentTarget.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            e.currentTarget.style.setProperty('--x', `${x}px`);
            e.currentTarget.style.setProperty('--y', `${y}px`);
              }}
            >
              Перейти к абонентам
        </a>
      </div>
    </div>
  )
}

const styles = {
  wrapper: {
    width: '100vw',
    height: '100vh',
    position: 'relative',
    overflow: 'hidden',
    background: '#060010',
    fontFamily: 'Inter, system-ui, -apple-system, BlinkMacSystemFont, sans-serif'
  },

  card: {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',

    background: 'none',
    backdropFilter: 'blur(32px)',
    WebkitBackdropFilter: 'blur(8px)',

    borderRadius: '40px',
    padding: '64px 56px',
    textAlign: 'center',
    color: '#EAE4E4',

    boxShadow: '0 30px 80px rgba(0,0,0,0.55)'
  },

  title: {
    margin: 0,
    fontSize: '36px',
    fontWeight: 700
  },

  subtitle: {
    marginTop: '16px',
    fontSize: '16px',
    opacity: 0.5,
    maxWidth: '460px'
  },

  button: {
    display: 'inline-block',
    marginTop: '28px',
    padding: '24px 48px',
    borderRadius: '200px',

    background: 'rgba(6, 0, 16, 0.65)',
    color: '#fff',
    textDecoration: 'none',
    fontWeight: 600,
    fontSize: '16px',

    transition: 'transform .15s ease, box-shadow .15s ease'
  }
}