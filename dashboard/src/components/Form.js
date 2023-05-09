import React from "react";

export default function Form(props) {    
    return (
        <form onSubmit={props.handleSubmit}>
          <div className="form-row">
            <div className="form-group">
              <h2 className="label-wrapper">
                <label htmlFor="dashboard-input" className="label__lg">
                  Input trader id
                </label>
              </h2>
              <input 
                type="text"
                id="dashboard-input"
                className="input"
                name="trader_id"
                autoComplete="off"
                value={props.traderId}
                onChange={props.handleChange}
              />
            </div>
            <div className="form-group">
              <h2 className="label-wrapper">
                <label htmlFor="delivery-day" className="label__lg">
                  Choose a date
                </label>
              </h2>
              <input 
                type="date" 
                id="delivery-day"
                className="input"
                name="delivery_day"
                value={props.deliveryDate}
                onChange={props.handleChange}
              />
            </div>
            <div className="form-btn">
              <button type="submit" className="btn btn__primary btn__lg">Generate</button>
            </div>
          </div>
        
      </form>
    );
}