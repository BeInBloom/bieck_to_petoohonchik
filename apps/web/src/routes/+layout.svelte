<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';
	import { onMount } from 'svelte';
	import { authSession } from '$lib/auth/session';

	let { children } = $props();

	onMount(() => void authSession.refresh());
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>
{@render children()}
