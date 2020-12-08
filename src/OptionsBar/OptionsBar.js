import React, { useState } from 'react';
import ValidationTextFields from './TextFieldMUI.js';


function OptionsBar() {

//get random stock on load....

const RandomStock = 'TSLA' // temp value

const [stock, setStock] = useState(RandomStock);
const [period, setPeriod] = useState(1) //days


  return (
    <div className="optionsbarsubgrid">
      <div className = "search">
        <ValidationTextFields>
        </ValidationTextFields>
      </div>
      <div className = "time">
      </div>
    </div>
  );
}

export default OptionsBar;

