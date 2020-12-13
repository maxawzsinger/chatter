import React, { useState } from 'react';
import ValidationTextFields from './TextFieldMUI.js';


function OptionsBar() {

//get random stock on load....

const RandomStock = 'TSLA' // temp value

const [stock, setStock] = useState(RandomStock);
const [period, setPeriod] = useState(1) //days


  return (
    <div className = "optionsbar">
      <div className = "search">
        <ValidationTextFields>
        </ValidationTextFields>
      </div>
      <div className = "time">
        <ValidationTextFields>
        </ValidationTextFields>
      </div>
    </div>
  );
}

export default OptionsBar;

