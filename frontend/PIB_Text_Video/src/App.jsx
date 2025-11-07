import './App.css'
import PressList from './components/PressList.jsx';
function App() {

  return (
    <div>
      <div className='header'>
        < img src="/emblem.png" alt="Emblem" id='leftimg' />
        <div className="titles">
        <h1 id='title'>Press Information Bureau</h1>
        <h2 id='title2'>Info to video</h2></div>
         <img src="/pib.jpg" alt="PIB logo" id='rightimg'/>
      </div>
      <PressList/>
    </div>
  )
}

export default App
