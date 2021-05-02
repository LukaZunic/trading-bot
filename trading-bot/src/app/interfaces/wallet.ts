export interface Wallet {
    balance: Number,
    crypto: Array<{
        name: String,
        value: Number,
        amount: Number
    }>
}
