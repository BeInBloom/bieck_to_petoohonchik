<script lang="ts">
	import type { Snippet } from 'svelte';

	let { narrow = false, children }: { narrow?: boolean; children: Snippet } = $props();
</script>

<div class:narrow class="page-container">
	{@render children()}
</div>

<style>
	.page-container {
		width: 100%;
		max-width: 72rem;
		margin: 0 auto;
		padding: 0 1rem;
	}

	.page-container.narrow {
		max-width: 36rem;
	}

	@media (min-width: 640px) {
		.page-container {
			padding: 0 1.5rem;
		}
	}
</style>
