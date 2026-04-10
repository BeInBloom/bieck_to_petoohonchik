import { writable, type Readable } from 'svelte/store';

import { AuthApi, type CurrentUser, type LoginInput, type RegisterInput } from '$lib/api/auth';
import { ApiError } from '$lib/api/client';

export interface AuthSessionState {
	user: CurrentUser | null;
	isLoading: boolean;
	isInitialized: boolean;
}

export interface AuthSession extends Readable<AuthSessionState> {
	refresh(): Promise<CurrentUser | null>;
	login(input: LoginInput): Promise<CurrentUser>;
	register(input: RegisterInput): Promise<CurrentUser>;
	logout(): Promise<void>;
}

const initialState: AuthSessionState = {
	user: null,
	isLoading: false,
	isInitialized: false
};

export class AuthSessionStore implements AuthSession {
	readonly #authApi: AuthApi;
	readonly #store = writable<AuthSessionState>(initialState);
	#requestId = 0;

	constructor(authApi: AuthApi = new AuthApi()) {
		this.#authApi = authApi;
	}

	public subscribe: AuthSession['subscribe'] = this.#store.subscribe;

	public async refresh(): Promise<CurrentUser | null> {
		const requestId = this.startRequest();

		try {
			return await this.tryRefresh(requestId);
		} catch (err) {
			return this.handleRefreshErr(err, requestId);
		}
	}

	public async login(input: LoginInput): Promise<CurrentUser> {
		const requestId = this.startRequest();

		try {
			return await this.tryLogin(input, requestId);
		} catch (err) {
			return this.handleErr(err, requestId);
		}
	}

	public async register(input: RegisterInput): Promise<CurrentUser> {
		const requestId = this.startRequest();

		try {
			return await this.tryRegister(input, requestId);
		} catch (err) {
			return this.handleErr(err, requestId);
		}
	}

	public async logout(): Promise<void> {
		const requestId = this.startRequest();

		try {
			await this.tryLogout(requestId);
		} catch (err) {
			this.handleErr(err, requestId);
		}
	}

	private async tryLogout(requestId: number): Promise<void> {
		await this.#authApi.logout();
		this.setAnonymous(requestId);
	}

	private tryRegister(input: RegisterInput, requestId: number): Promise<CurrentUser> {
		return this.runAuthAction(() => this.#authApi.register(input), requestId);
	}

	private tryLogin(input: LoginInput, requestId: number): Promise<CurrentUser> {
		return this.runAuthAction(() => this.#authApi.login(input), requestId);
	}

	private tryRefresh(requestId: number): Promise<CurrentUser> {
		return this.runAuthAction(() => this.#authApi.getCurrentUser(), requestId);
	}

	private async runAuthAction(
		action: () => Promise<CurrentUser>,
		requestId: number
	): Promise<CurrentUser> {
		const user = await action();
		this.setAuthenticated(user, requestId);
		return user;
	}

	private setAuthenticated(user: CurrentUser, requestId: number): void {
		if (!this.isCurrentRequest(requestId)) return;

		this.#store.set({
			user,
			isLoading: false,
			isInitialized: true
		});
	}

	private setAnonymous(requestId: number): void {
		if (!this.isCurrentRequest(requestId)) return;

		this.#store.set({
			user: null,
			isLoading: false,
			isInitialized: true
		});
	}

	private handleErr(err: unknown, requestId: number): never {
		if (this.isCurrentRequest(requestId)) this.setLoading(false);
		throw err;
	}

	private handleRefreshErr(err: unknown, requestId: number): null {
		if (err instanceof ApiError && err.status === 401) {
			this.setAnonymous(requestId);
			return null;
		}

		if (this.isCurrentRequest(requestId)) this.setLoading(false);
		throw err;
	}

	private startRequest(): number {
		this.#requestId += 1;
		this.setLoading(true);
		return this.#requestId;
	}

	private isCurrentRequest(requestId: number): boolean {
		return requestId === this.#requestId;
	}

	private setLoading(isLoading: boolean): void {
		this.#store.update((state) => ({
			...state,
			isLoading
		}));
	}
}

export const authSession = new AuthSessionStore();
