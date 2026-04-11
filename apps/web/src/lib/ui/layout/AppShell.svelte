<script lang="ts">
	import type { CurrentUser } from '$lib/api/auth';
	import type { Snippet } from 'svelte';
	import AppHeader from './AppHeader.svelte';

	let { user = null, children }: { user?: CurrentUser | null; children: Snippet } = $props();
</script>

<div class="app-shell">
	<AppHeader {user} />

	<main class="app-shell__main">
		{@render children()}
	</main>
</div>
