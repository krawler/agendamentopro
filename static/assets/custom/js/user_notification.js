$(document).ready(function(){

    Notification.requestPermission().then(permission => {
         if (permission === 'granted') {
             console.log('Permissão concedida');
         } else {
             console.log('Permissão negada');
         }
     }).then(() => {
         if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('http://localhost:8000/static/assets/custom/js/service-worker.js') // Certifique-se de que o caminho está correto
              .then(registration => {
                  console.log('Service Worker registrado com sucesso:', registration);
                  registration.pushManager.subscribe({
                    userVisibleOnly: true,
                    applicationServerKey: 'MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEBo2IVqQCPLIRENnN0eJDA1mILELPv6Qo4CLr_KcbnXrFfYVJHKlxHe71JrXy-PZm-IOdLqTg6WKGKqFuizz10g' // Substitua pela sua chave pública VAPID
                  }).then(subscription => {
                        // Obtenha as informações de assinatura
                        const endpoint = subscription.endpoint;
                        const p256dh = subscription.getKey('p256dh');
                        const auth = subscription.getKey('auth');
                    
                        const subscriptionData = {
                          endpoint: endpoint,
                          keys: {
                            p256dh: arrayBufferToBase64(p256dh), // Converta ArrayBuffer para Base64
                            auth: arrayBufferToBase64(auth)     // Converta ArrayBuffer para Base64
                          }
                        };                    

                        fetch('http://localhost:8000/perfil/save-subscription/', {
                          method: 'POST',
                          headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCookie('csrftoken') // Se o CSRF estiver habilitado
                          },
                          body: JSON.stringify(subscriptionData)
                        }).then(response => {
                          if (response.ok) {
                            console.log('Assinatura salva com sucesso!');
                          } else {
                            console.error('Erro ao salvar assinatura:', response.status);
                          }
                        }).catch(error => {
                          console.error('Erro na requisição:', error);
                        });
                    
                      }).catch(error => {
                        console.error('Erro ao obter assinatura:', error);
                      });
                })
              .catch(error => {
                  console.error('Erro ao registrar Service Worker:', error);
              });            
         }
     });
  
      // Função para converter ArrayBuffer para Base64
      function arrayBufferToBase64(buffer) {
        let binary = '';
        const bytes = new Uint8Array(buffer);
        const len = bytes.byteLength;
        for (let i = 0; i < len; i++) {
          binary += String.fromCharCode(bytes[i]);
        }
        return btoa(binary);
      }
      
      // Função para obter o cookie CSRF (se necessário)
      function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
            }
          }
        }
        return cookieValue;
      }

 });

  // Exibir notificação
  function showNotification() {
     const notification = new Notification('Título da notificação', {
         body: 'Corpo da notificação',
         icon: 'agendamentopro/imagens/logo_cortado.png'
     });
 }
