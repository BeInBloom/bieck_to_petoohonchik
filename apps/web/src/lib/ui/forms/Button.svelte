<script lang="ts">
	import type { Snippet } from 'svelte';

	type ButtonVariant = 'primary' | 'secondary';

	let {
		type = 'button',
		variant = 'primary',
		disabled = false,
		children
	}: {
		type?: 'button' | 'submit';
		variant?: ButtonVariant;
		disabled?: boolean;
		children: Snippet;
	} = $props();
</script>

<button class={`button button--${variant}`} {type} {disabled}>
	{@render children()}
</button>

<style>
	.button {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		min-height: 44px;
		padding: 0.75rem 1rem;
		border: 1px solid transparent;
		border-radius: var(--radius);
		font: inherit;
		font-size: 0.95rem;
		font-weight: 600;
		line-height: 1;
		cursor: pointer;
		transition:
			background-color 120ms ease,
			border-color 120ms ease,
			color 120ms ease,
			opacity 120ms ease;
	}

	.button:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	.button--primary {
		background: var(--primary);
		color: #fff;
	}

	.button--primary:hover:enabled {
		background: var(--primary-hover);
	}

	.button--secondary {
		border-color: var(--border);
		background: var(--surface);
		color: var(--text);
	}
</style>
