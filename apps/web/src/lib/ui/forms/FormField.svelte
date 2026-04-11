<script lang="ts">
	import type { Snippet } from 'svelte';

	let {
		id,
		label,
		hint,
		children
	}: {
		id: string;
		label: string;
		hint?: string;
		children: Snippet;
	} = $props();
</script>

<div class="form-field">
	<label class="form-field__label" for={id}>{label}</label>

	<div class="form-field__control">
		{@render children()}
	</div>

	{#if hint}
		<p class="form-field__hint">{hint}</p>
	{/if}
</div>

<style>
	.form-field {
		display: grid;
		gap: 0.5rem;
	}

	.form-field__label {
		font-size: 0.95rem;
		font-weight: 600;
		color: var(--text);
	}

	.form-field__hint {
		margin: 0;
		font-size: 0.875rem;
		color: var(--text-muted);
	}
</style>
