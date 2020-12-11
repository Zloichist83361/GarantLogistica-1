 const container_status = document.querySelector('.container-status');
 const container_status_none = document.querySelector('.container-status-none');

 function do_ajax() {
        var req = new XMLHttpRequest();
        var statustext1 = document.getElementById('status_1');
        var statustext2 = document.getElementById('status_2');
        var statustext3 = document.getElementById('status_3');
        var statustext4 = document.getElementById('status_4');
        var statustext5 = document.getElementById('status_5');
        var statustextNone = document.getElementById('status_none');
        req.onload = function()

        { console.log(this.responseText);
          var response = JSON.parse(this.responseText);
          if(response.order_status && response.date_order_users) {

            //result.innerHTML = "На " + response.date_order_users + " статус: " + response.order_status;
            container_status.classList.contains('open') ? container_status.classList.remove('open') : container_status.classList.add('open');
          } else {
            //result.innerHTML = "Нихуя";
            container_status_none.classList.contains('open') ? container_status_none.classList.remove('open') : container_status_none.classList.add('open');
          }
        }
        req.open('GET', '/tracking/status?' + "tracknumber=" + document.getElementById('tracking-input').value, true);
        req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
        req.send();

      }