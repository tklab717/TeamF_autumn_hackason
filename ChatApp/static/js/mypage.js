document.getElementById('team-select-form').onsubmit = function(event) {
    // 必要な値が入力されているかチェックする
    const year = document.getElementById('year').value;
    const season = document.getElementById('season').value;
    const team = document.getElementById('team').value;
    const github = document.getElementById('github').value;
    
    if (!year || !season || !team || !github) {
      event.preventDefault();
      alert('全ての項目を入力してください。');
    }
  };
  