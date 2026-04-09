<script lang="ts">
	type ActionLink = {
		label: string;
		href: string;
		variant?: 'primary' | 'secondary';
	};

	type CtaSectionProps = {
		eyebrow?: string;
		title: string;
		description: string;
		primaryAction: ActionLink;
		secondaryAction?: ActionLink;
		note?: string;
	};

	let { eyebrow, title, description, primaryAction, secondaryAction, note }: CtaSectionProps =
		$props();
</script>

<section class="cta-section" aria-labelledby="cta-title">
	<div class="cta-section__inner">
		<div class="cta-section__content">
			{#if eyebrow}
				<p class="cta-section__eyebrow">{eyebrow}</p>
			{/if}

			<h2 id="cta-title" class="cta-section__title">{title}</h2>

			{#if description}
				<p class="cta-section__description">{description}</p>
			{/if}

			<div class="cta-section__actions">
				<a class="cta-section__button cta-section__button--primary" href={primaryAction.href}>
					{primaryAction.label}
				</a>

				{#if secondaryAction}
					<a class="cta-section__button cta-section__button--secondary" href={secondaryAction.href}>
						{secondaryAction.label}
					</a>
				{/if}
			</div>

			{#if note}
				<p class="cta-section__note">{note}</p>
			{/if}
		</div>
	</div>
</section>
