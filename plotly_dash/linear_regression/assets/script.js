const refresh = setInterval(() => {
  const explanatory = document.querySelectorAll(`.explanatory-radio
  input[type="radio"]`);
  const response = document.querySelectorAll(`.response-radio 
  input[type="radio"]`);
  if (explanatory.length > 0 && response.length > 0) {
    clearInterval(refresh);
  }
  // Including the default checked radio buttons on load, ensure that the user
  // can never select the same two variables at once.
  explanatory.forEach((radio, index) => {
    if (radio.checked) {
      response[index].disabled = true;
    }

    radio.addEventListener('change', () => {
      response.forEach((radio) => {
        radio.disabled = false;
      });

      response[index].disabled = true;
    });
  });
  response.forEach((radio, index) => {
    if (radio.checked) {
      explanatory[index].disabled = true;
    }

    radio.addEventListener('change', () => {
      explanatory.forEach((radio) => {
        radio.disabled = false;
      });

      explanatory[index].disabled = true;
    });
  });
}, 250);
