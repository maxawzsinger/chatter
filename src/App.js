import logo from './logo.svg';
import OptionsBar from './OptionsBar/OptionsBar.js'
import './styles.css'


function App() {
  return (
    <div className="wrapper">
      <div className = "titlebar">
      </div>
      <div className = "optionsbar">
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

