const refresh = setInterval(() => {
  const firstExplanatory = document.querySelectorAll(`.first-explanatory-radio
  input[type="radio"]`);
  const secondExplanatory = document.querySelectorAll(`
  .second-explanatory-radio input[type="radio"]`);
  const response = document.querySelectorAll(`.response-radio 
  input[type="radio"]`);
  if (
    firstExplanatory.length > 0 && secondExplanatory > 0 && response.length > 0
    ) {
    clearInterval(refresh);
  }
  // Including the default checked radio buttons on load, ensure that the user
  // can never select the same two or three variables at once.
  firstExplanatory.forEach((radio, index) => {
    if (radio.checked) {
      secondExplanatory[index].disabled = true;
      response[index].disabled = true;
    }

    radio.addEventListener('change', () => {
      secondExplanatory.forEach((radio) => {
        radio.disabled = false;
      });
      response.forEach((radio) => {
        radio.disabled = false;
      });

      secondExplanatory[index].disabled = true;
      response[index].disabled = true;
    });
  });
  secondExplanatory.forEach((radio, index) => {
    if (radio.checked) {
      firstExplanatory[index].disabled = true;
      response[index].disabled = true;
    }

    radio.addEventListener('change', () => {
      firstExplanatory.forEach((radio) => {
        radio.disabled = false;
      });
      response.forEach((radio) => {
        radio.disabled = false;
      });

      firstExplanatory[index].disabled = true;
      response[index].disabled = true;
    });
  });
  response.forEach((radio, index) => {
    if (radio.checked) {
      firstExplanatory[index].disabled = true;
      secondExplanatory[index].disabled = true;
    }

    radio.addEventListener('change', () => {
      firstExplanatory.forEach((radio) => {
        radio.disabled = false;
      });
      secondExplanatory.forEach((radio) => {
        radio.disabled = false;
      });

      firstExplanatory[index].disabled = true;
      secondExplanatory[index].disabled = true;
    });
  });
}, 250);
