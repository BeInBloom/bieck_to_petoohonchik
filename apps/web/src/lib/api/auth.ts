import { ApiClient } from './client';

export type UserRole = 'user' | 'staff';

export interface CurrentUser {
	id: number;
	email: string;
	display_name: string;
	role: UserRole;
	is_active: boolean;
	created_at: string;
	updated_at: string;
}

export interface RegisterInput {
	email: string;
	display_name: string;
	password: string;
}

export interface LoginInput {
	email: string;
	password: string;
}

interface AuthResponse {
	user: CurrentUser;
}

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
