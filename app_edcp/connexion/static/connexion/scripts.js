
  $(document).ready(function() {
    // Select the password field by its name attribute
    var passwordField = $('input[name="password1"]');
    var confirmPassword = $('input[name="password2"]');
    var btnSubmit = $('#btn-submit');
    // Create the password strength indicator element
    var strengthIndicator = $('<div id="password-strength" class="mt-2"></div>');
    var passwordMatch = $('<div id="password-match" class="mt-2 text-danger"></div>');
    // Append the strength indicator after the password field
    passwordField.after(strengthIndicator);
    confirmPassword.after(passwordMatch);

    passwordField.on('input', function() {
      var password = $(this).val();
      var strength = calculatePasswordStrength(password);
      strengthIndicator.text('Force du mot de passe : ' + strength.text).attr('class', strength.class);
    });

    confirmPassword.on('input', function(){
      var password1 = passwordField.val();
      var password2 = confirmPassword.val();
      if(password1 != password2){
        passwordMatch.text('Les mots de passe ne correspondent pas.');
        btnSubmit.prop('disabled', true);
      }
      else{
        passwordMatch.text('');
        btnSubmit.prop('disabled', false);
      }
    });

    function calculatePasswordStrength(password) {
      var strength = 0;
      if (password.length >= 6) {
          strength += 1;
      }
      if (password.match(/[A-Z]/)) {
          strength += 1;
      }
      if (password.match(/[a-z]/)) {
          strength += 1;
      }
      if (password.match(/[0-9]/)) {
          strength += 1;
      }
      if (password.match(/[\W_]/)) {
          strength += 1;
      }
      switch (strength) {
        case 0:
        case 1:
            return { text: 'Très faible', class: 'very-weak' };
        case 2:
            return { text: 'Faible', class: 'weak' };
        case 3:
            return { text: 'Moyenne', class: 'moderate' };
        case 4:
            return { text: 'Forte', class: 'strong' };
        case 5:
            return { text: 'Très forte', class: 'very-strong' };
      }
    }
  });