//import React from 'react';
//import logo from './logo.svg';
import  Home from './pages/Home';
import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.tsx</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

//export default App;

export default function App() {
  return (
    <div className="min-h-screen" style={{ padding: 16 }}>
      <h1>Osobni asistent za vremensku prognozu *Vakula 2.0*</h1>
      <Home />
    </div>
  );
}