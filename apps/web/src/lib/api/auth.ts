import type { components } from '@pets/api-types';

import { ApiClient } from './client';

export type UserRole = components['schemas']['UserRole'];
export type CurrentUser = components['schemas']['UserRead'];
export type RegisterInput = components['schemas']['RegisterRequest'];
export type LoginInput = components['schemas']['LoginRequest'];

type AuthResponse = components['schemas']['AuthResponse'];

export class AuthApi {
	readonly #client: ApiClient;

	constructor(client: ApiClient = new ApiClient()) {
		this.#client = client;
	}

	public async register(input: RegisterInput): Promise<CurrentUser> {
		const res = await this.#client.post<AuthResponse>('/auth/register', input);
		return res.user;
	}

	public async login(input: LoginInput): Promise<CurrentUser> {
		const res = await this.#client.post<AuthResponse>('/auth/login', input);
		return res.user;
	}

	public async logout(): Promise<void> {
		await this.#client.post<void>('/auth/logout');
	}

	public getCurrentUser(): Promise<CurrentUser> {
		return this.#client.get<CurrentUser>('/auth/me');
	}
}
