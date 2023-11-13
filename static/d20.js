function findRolls() {
	const tags = ['p', 'th', 'td'];
	const re = new RegExp("([0-9]*)d([0-9]+)( ?(\\+|\\-) ?(\\-?[0-9]+))?", 'g');
	for (tag of tags) {
		for (elem of document.body.getElementsByTagName(tag)) {
			elem.innerHTML = elem.innerHTML.replaceAll(re, addSpanToRollText)
		}
	}
}

function addSpanToRollText(match, p1, p2, p3, p4, p5, offset, string) {
	// span = document.createElement('span')
	// span.classList.add('roll')
	//span.onclick = runRoll(match)
	// span.innerText = match
	// return(span)

	count = (p1 === '') ? '1': p1
	sides = p2
	operator = (typeof p4 === 'undefined') ? '+': p4
	modifier = (typeof p5 === 'undefined') ? '0': p5

	return('<span class="roll" style="cursor: pointer;" onclick="runRoll(\''+count+'\', \''+sides+'\', \''+operator+'\', \''+modifier+'\')">'+match+'</span>')
}

function runRoll(count, sides, operator, modifier) {
	count = parseInt(count)
	sides = parseInt(sides)
	modifier = parseInt(modifier)

	let rolls = []
	let total = 0
	for (let step = 0; step < count; step++) {
		var temp = randomInt(1, sides)
		rolls.push(temp)
		total += temp
	}

	if (operator == '-') {
		total -= modifier
	}
	else if (operator == '+') {
		total += modifier
	}
	str = count + 'd' + sides
	if (modifier !== 0) {
		str += operator + modifier
	}
	alert(str + ' = '+ total + '\n[' + rolls + ']')
}

function randomInt(min, max) {
	min = Math.ceil(min);
	max = Math.floor(max);
	return Math.floor(Math.random() * (max-min+1) + min)
}

if (typeof window.onload == 'function') {
	var oldonload = window.onload
	window.onload = function() {
		oldonload();
		findRolls();
	}
} else {
	window.onload == findRolls;
}

// window.onload = function() { 
// 	findRolls();
// }