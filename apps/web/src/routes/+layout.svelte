<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';
	import { onMount } from 'svelte';
	import { authSession } from '$lib/auth/session';
	import AppShell from '$lib/ui/layout/AppShell.svelte';

	let { children } = $props();

	onMount(() => void authSession.refresh());
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>

<AppShell user={$authSession.user}>
	{@render children()}
</AppShell>
