<script lang="ts">
	import { homePage } from '$lib/content/home';
	import HeroSection from '$lib/ui/home/HeroSection.svelte';
	import FeatureGrid from '$lib/ui/home/FeatureGrid.svelte';
	import CtaSection from '$lib/ui/home/CtaSection.svelte';
</script>

<HeroSection {...homePage.hero} />
<FeatureGrid {...homePage.features} />
<CtaSection {...homePage.cta} />
