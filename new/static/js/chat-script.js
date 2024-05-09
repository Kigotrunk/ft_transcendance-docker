const button = document.querySelector('.send-button');
const input = document.querySelector('.text-input');

const talkContainer = document.querySelector('.talk');
talkContainer.scrollTop = talkContainer.scrollHeight;

input.addEventListener('input', () => {
	console.log("change");
	if (input.value === '')
		button.disabled = true;
	else
		button.disabled = false;
});
