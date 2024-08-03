/**
 * Permet de rechercher dans la base de données si l'adresse email saisie existe déjà
 */
/* document.addEventListener('DOMContentLoaded', function() {
  const fieldEmail = document.getElementById('id_email');
  const divNotAvailable = document.getElementById('email-not-available');
  const divAvailable = document.getElementById('email-available');
  const btnSubmit = document.getElementById('btn-submit')

  function showMessage(email_exists) {
    if(email_exists){
      divNotAvailable.style.display = 'block'
      divAvailable.style.display = 'none'
      btnSubmit.style.display = 'none'
    }
    else {
      divNotAvailable.style.display = 'none'
      divAvailable.style.display = 'block'
      btnSubmit.style.display = 'block'
    }
  }

  fieldEmail.addEventListener('change', function() {
    // console.log('change event fired : ');
    const email = fieldEmail.value;
    fetch(`?email=${email}`, {
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    }).then(response => response.json())
    .then(data => {
      // console.log('data : ', data);
      showMessage(data.email_exists);
    });
  });

  // fieldTypeClient.addEventListener('change', toggleFields);
  // toggleFields();  // Initial call to set correct fields on load
}); */

$(document).ready(function() {
  // HTML elements
  const $fieldEmail = $('#id_email');
  const $divNotAvailable = $('#email-not-available');
  const $divAvailable = $('#email-available');
  const $btnSubmitDesignation = $('#btn-submit-desigation');

  const $fieldIsDPO = $('#id_user_is_dpo_0');
  const $fieldIsNotDPO = $('#id_user_is_dpo_1');
  const $btnSubmitIsDPO = $('#btn-submit-is-dpo');
  const $formDesignation = $('#designation-form');


  // functions
  function showMessage(email_exists) {
    if(email_exists){
      $divNotAvailable.show();
      $divAvailable.hide();
      $btnSubmitDesignation.hide();
    } else {
      $divNotAvailable.hide();
      $divAvailable.show();
      $btnSubmitDesignation.show();
    }
  }

  function toggleForm(){
    if($fieldIsDPO.is(':checked')){
      $btnSubmitIsDPO.show();
      $formDesignation.hide();
    } else if($fieldIsNotDPO.is(':checked')){
      $btnSubmitIsDPO.hide();
      $formDesignation.show();
    } 
  }

  // events
  $fieldEmail.on('change', function() {
    const email = $fieldEmail.val();
    $.ajax({
      url: '',
      data: { email: email },
      headers: { 'X-Requested-With': 'XMLHttpRequest' },
      success: function(data) {
        showMessage(data.email_exists);
      }
    });
  });

  $fieldIsDPO.on('change', toggleForm);
  $fieldIsNotDPO.on('change', toggleForm);
  toggleForm();
  


  // $('#fieldTypeClient').on('change', toggleFields);
  // toggleFields();  // Initial call to set correct fields on load
});