import Home from './pages/Home';
import './App.css';

export default function App() {
  return (
    <main className="app">
      <header className="app-header">
        <h1>Vakula 2.0</h1>
        <p className="muted">Osobni asistent za vremensku prognozu</p>
      </header>
      <Home />
    </main>
  );
}
