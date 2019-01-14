#/* Copyright (C) Florentina Petcu - All Rights Reserved
# * Unauthorized copying of this file, via any medium is strictly prohibited
# * Proprietary and confidential
# * Written by Florentina Petcu <florentina.ptc@gmail.com>, December 2018
# */

import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';


class AppTitle extends React.Component {
  render() {
    return (
      <div className="title">
        <h1>ALLERGY AND MEDICINE</h1>
      </div>
    );
  }
}

class OptionButtons extends React.Component {
  constructor(props) {
      super(props);

      this.state = {
        listValues: [],
        selectedType: '',
        resultValue: ''
      };

      this.allAllergies = this.allAllergies.bind(this);
      this.allMedicines = this.allMedicines.bind(this);
      this.getResult = this.getResult.bind(this);
   }

   allAllergies() {
    this.setState({ selectedType: 'allergy' })
    fetch("http://127.0.0.1:5000/allAllergies")
    .then(response => response.json())
    .then(data => this.setState({ listValues: data['result'] }));
  }

  allMedicines() {
    this.setState({ selectedType: 'medicine' })
    fetch("http://127.0.0.1:5000/allMedicines")
    .then(response => response.json())
    .then(data => this.setState({ listValues: data['result'] }));
  }

  getResult(e) {
    const aux = e.target.textContent;
    if (this.state.selectedType == 'allergy') {
      fetch("http://127.0.0.1:5000/medicineByAllergy", {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({'allergyName': aux})
      })
      .then(response => response.json())
      .then(data => this.setState({ resultValue: data[aux][0] }));
    } 

    if (this.state.selectedType == 'medicine') {
      fetch("http://127.0.0.1:5000/allergyByMedicine", {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({'medicineName': aux})
      })
      .then(response => response.json())
      .then(data => this.setState({ resultValue: data[aux][0] }));
    }
  }

  render() {
    return (
      <div>
      <div className='optionsBtn'>
        <div className='optionsCaption'>
        </div>
        <button 
            className="w3-btn w3-black allergyBtn"
            type="button"
            onClick={this.allAllergies} >
            Allergy
          </button>
          <button 
            className="w3-btn w3-black medicineBtn"
            type="button"
            onClick={this.allMedicines} >
            Medicine
          </button>
      </div>


          <div className="result column">
            <b>{ this.state.resultValue }</b>
          </div>

      <div class="row">
        <div className='listValues column'>
            {this.state.listValues.map((pp, index) => {
              return (
                <div 
                  className='listBtn' 
                  onClick={this.getResult}
                  key={index}>
                    {pp}
                </div>
                )
              })
            }
          </div>

        </div>
      </div>
    );
  }
}

class App extends Component {
  render() {
    return (  
      <div className="App">
        <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css" />
      
        <AppTitle />
        <OptionButtons />
      </div>
    );
  }
}

export default App;
