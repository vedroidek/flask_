function show_date(name) {
    document.getElementById('time').style.display = "none";
    document.getElementById('date').innerText = `${name}`;
    document.getElementById('date').style.color = 'yellow';
    setTimeout(() => document.getElementById('date').style.display = "none", 3000);
}