import logo from './logo.svg';
import OptionsBar from './OptionsBar/OptionsBar.js'
import './styles.css'


function App() {
  return (
    <div className="wrapper">
      <div className = "titlebar">
        tweets vs. stock
      </div>
      <div className = "options">
          <OptionsBar>
        </OptionsBar>      
      </div>

      <div className = "graph">
      </div>
      <div className = "legend">
      </div>
    </div>
  );
}

export default App;

