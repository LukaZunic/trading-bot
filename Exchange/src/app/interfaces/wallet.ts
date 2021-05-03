export interface Wallet {
    balance: number;
    crypto: Array<{
        name: string;
        value: number;
        amount: number;
    }>;
}
