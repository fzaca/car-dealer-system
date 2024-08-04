document.addEventListener('DOMContentLoaded', function() {
  // Mobile selectors
  const mobileRangeInput = document.getElementById('mobile-price-range');
  const mobileMaxPriceInput = document.getElementById('mobile-max_price');

  const mobileMinYearRangeInput = document.getElementById('mobile-min_year_range');
  const mobileMaxYearRangeInput = document.getElementById('mobile-max_year_range');
  const mobileMinYearInput = document.getElementById('mobile-min_year');
  const mobileMaxYearInput = document.getElementById('mobile-max_year');

  // Desktop selectors
  const desktopRangeInput = document.getElementById('desktop-price-range');
  const desktopMaxPriceInput = document.getElementById('desktop-max_price');

  const desktopMinYearRangeInput = document.getElementById('desktop-min_year_range');
  const desktopMaxYearRangeInput = document.getElementById('desktop-max_year_range');
  const desktopMinYearInput = document.getElementById('desktop-min_year');
  const desktopMaxYearInput = document.getElementById('desktop-max_year');

  // Mobile Range Synchronization
  if (mobileRangeInput && mobileMaxPriceInput) {
    mobileRangeInput.addEventListener('input', function() {
      mobileMaxPriceInput.value = mobileRangeInput.value;
    });

    mobileMaxPriceInput.addEventListener('input', function() {
      if (parseInt(mobileMaxPriceInput.value) > mobileRangeInput.max) {
        mobileMaxPriceInput.value = mobileRangeInput.max;
      }
      mobileRangeInput.value = mobileMaxPriceInput.value;
    });
  }

  if (mobileMinYearRangeInput && mobileMaxYearRangeInput && mobileMinYearInput && mobileMaxYearInput) {
    mobileMinYearRangeInput.addEventListener('input', function() {
      mobileMinYearInput.value = mobileMinYearRangeInput.value;
      if (parseInt(mobileMinYearRangeInput.value) > parseInt(mobileMaxYearRangeInput.value)) {
        mobileMaxYearRangeInput.value = mobileMinYearRangeInput.value;
        mobileMaxYearInput.value = mobileMinYearRangeInput.value;
      }
    });

    mobileMinYearInput.addEventListener('input', function() {
      mobileMinYearRangeInput.value = mobileMinYearInput.value;
      if (parseInt(mobileMinYearInput.value) > parseInt(mobileMaxYearInput.value)) {
        mobileMaxYearRangeInput.value = mobileMinYearInput.value;
        mobileMaxYearInput.value = mobileMinYearInput.value;
      }
    });

    mobileMaxYearRangeInput.addEventListener('input', function() {
      mobileMaxYearInput.value = mobileMaxYearRangeInput.value;
      if (parseInt(mobileMaxYearRangeInput.value) < parseInt(mobileMinYearRangeInput.value)) {
        mobileMinYearRangeInput.value = mobileMaxYearRangeInput.value;
        mobileMinYearInput.value = mobileMaxYearRangeInput.value;
      }
    });

    mobileMaxYearInput.addEventListener('input', function() {
      mobileMaxYearRangeInput.value = mobileMaxYearInput.value;
      if (parseInt(mobileMaxYearInput.value) < parseInt(mobileMinYearInput.value)) {
        mobileMinYearRangeInput.value = mobileMaxYearInput.value;
        mobileMinYearInput.value = mobileMaxYearInput.value;
      }
    });
  }

  // Desktop Range Synchronization
  if (desktopRangeInput && desktopMaxPriceInput) {
    desktopRangeInput.addEventListener('input', function() {
      desktopMaxPriceInput.value = desktopRangeInput.value;
    });

    desktopMaxPriceInput.addEventListener('input', function() {
      if (parseInt(desktopMaxPriceInput.value) > desktopRangeInput.max) {
        desktopMaxPriceInput.value = desktopRangeInput.max;
      }
      desktopRangeInput.value = desktopMaxPriceInput.value;
    });
  }

  if (desktopMinYearRangeInput && desktopMaxYearRangeInput && desktopMinYearInput && desktopMaxYearInput) {
    desktopMinYearRangeInput.addEventListener('input', function() {
      desktopMinYearInput.value = desktopMinYearRangeInput.value;
      if (parseInt(desktopMinYearRangeInput.value) > parseInt(desktopMaxYearRangeInput.value)) {
        desktopMaxYearRangeInput.value = desktopMinYearRangeInput.value;
        desktopMaxYearInput.value = desktopMinYearRangeInput.value;
      }
    });

    desktopMinYearInput.addEventListener('input', function() {
      desktopMinYearRangeInput.value = desktopMinYearInput.value;
      if (parseInt(desktopMinYearInput.value) > parseInt(desktopMaxYearInput.value)) {
        desktopMaxYearRangeInput.value = desktopMinYearInput.value;
        desktopMaxYearInput.value = desktopMinYearInput.value;
      }
    });

    desktopMaxYearRangeInput.addEventListener('input', function() {
      desktopMaxYearInput.value = desktopMaxYearRangeInput.value;
      if (parseInt(desktopMaxYearRangeInput.value) < parseInt(desktopMinYearRangeInput.value)) {
        desktopMinYearRangeInput.value = desktopMaxYearRangeInput.value;
        desktopMinYearInput.value = desktopMaxYearRangeInput.value;
      }
    });

    desktopMaxYearInput.addEventListener('input', function() {
      desktopMaxYearRangeInput.value = desktopMaxYearInput.value;
      if (parseInt(desktopMaxYearInput.value) < parseInt(desktopMinYearInput.value)) {
        desktopMinYearRangeInput.value = desktopMaxYearInput.value;
        desktopMinYearInput.value = desktopMaxYearInput.value;
      }
    });
  }
});
