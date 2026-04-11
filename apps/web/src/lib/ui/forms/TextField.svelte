<script lang="ts">
	import type { FullAutoFill } from 'svelte/elements';

	let {
		id,
		name,
		type = 'text',
		value = '',
		placeholder = '',
		autocomplete,
		disabled = false
	}: {
		id: string;
		name: string;
		type?: string;
		value?: string;
		placeholder?: string;
		autocomplete?: FullAutoFill;
		disabled?: boolean;
	} = $props();
</script>

<input class="text-field" {id} {name} {type} {value} {placeholder} {autocomplete} {disabled} />

<style>
	.text-field {
		width: 100%;
		min-height: 44px;
		padding: 0.75rem 0.875rem;
		border: 1px solid var(--border);
		border-radius: var(--radius);
		background: var(--surface);
		color: var(--text);
		font: inherit;
		font-size: 0.95rem;
		line-height: 1.4;
		box-sizing: border-box;
	}

	.text-field::placeholder {
		color: var(--text-muted);
	}

	.text-field:focus {
		outline: 2px solid color-mix(in srgb, var(--primary) 20%, transparent);
		outline-offset: 1px;
		border-color: var(--primary);
	}
</style>
