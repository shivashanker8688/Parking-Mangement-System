document.getElementById('loginForm').addEventListener('submit', function(event) { 
    event.preventDefault(); 
    const name = document.getElementById('name').value; 
    const password = document.getElementById('password').value; 
 
    fetch('/login', { 
        method: 'POST', 
        headers: { 
            'Content-Type': 'application/json' 
        }, 
        body: JSON.stringify({ name, password }) 
    }).then(response => response.json()) 
    .then(data => { 
        if (data.message === 'Login successful!') { 
            document.querySelector('.login-form').style.display = 'none'; 
            document.getElementById('parkingSlots').style.display = 'block'; 
            updateParkingSlots(); 
        } else { 
            alert('Invalid login credentials'); 
        } 
    }); 
}); 
 
document.getElementById('signupBtn').addEventListener('click', function() { 
    document.querySelector('.login-form').style.display = 'none'; 
    document.getElementById('signupForm').style.display = 'block'; 
}); 
 
document.getElementById('backToLoginBtn').addEventListener('click', function() { 
    document.getElementById('signupForm').style.display = 'none'; 
    document.querySelector('.login-form').style.display = 'block'; 
34  
  
}); 
 
document.getElementById('registerForm').addEventListener('submit', function(event) { 
    event.preventDefault(); 
    const signupName = document.getElementById('signupName').value; 
    const signupPassword = document.getElementById('signupPassword').value; 
    const confirmPassword = document.getElementById('confirmPassword').value; 
    const email = document.getElementById('email').value; 
    const phone = document.getElementById('phone').value; 
    const history = document.getElementById('history').value; 
 
    if (signupPassword !== confirmPassword) { 
        alert('Passwords do not match'); 
        return; 
    } 
 
    fetch('/register', { 
        method: 'POST', 
        headers: { 
            'Content-Type': 'application/json' 
        }, 
        body: JSON.stringify({ name: signupName, password: signupPassword, email, phone, history }) 
    }).then(response => response.json()) 
    .then(data => { 
        alert(data.message); 
        document.getElementById('signupForm').style.display = 'none'; 
        document.querySelector('.login-form').style.display = 'block'; 
    }); 
}); 
 
function updateParkingSlots() { 
    fetch('/slots') 
    .then(response => response.json()) 
    .then(slots => { 
        slots.forEach(slot => { 
            const slotElement = document.getElementById(`slot${slot.slot_number}`); 
            slotElement.className = slot.occupied ? 'slot occupied' : 'slot not-occupied'; 
        }); 
    }); 
}
