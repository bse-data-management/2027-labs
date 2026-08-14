# Part C (optional) — The lost payout

Nothing here is examinable and nothing later in the course depends on it. Do it
if you finish Parts A and B early, or at home afterwards. It takes about ten
minutes and it is the one thing in this lab you have to *watch* rather than read.

Two people write to the same row at the same time. No error is raised, and €40
disappears.

You need **two terminals side by side**. In each one, from the repository root:

```bash
docker compose exec postgres psql -U labs -d labs
```

Call the left one **A** and the right one **B**. Keep both visible — the whole
point is what terminal B does at one particular moment.

## Setup (terminal A, once)

```sql
DROP TABLE IF EXISTS driver_balances;
CREATE TABLE driver_balances (
    driver_id integer PRIMARY KEY,
    balance   numeric(10,2) NOT NULL
);
INSERT INTO driver_balances VALUES (4471, 120.00);
```

Driver 4471 has **€120**. Two payouts are about to arrive: **€40** and **€25**.
The driver is owed 120 + 40 + 25 = **€185**.

Notice that each `UPDATE` below writes the *new total* rather than
`balance = balance + 40`. That is not a trick to make this fail — it is what most
applications do: read the balance, add the payout in Python, write the result
back. The arithmetic happens outside the database.

## Round 1 — no transactions

Run these in this exact order, alternating terminals.

**1. A reads.** A sees `120.00`, so payout A's new total is 160.

```sql
SELECT balance FROM driver_balances WHERE driver_id = 4471;
```

**2. B reads.** B also sees `120.00` — A has not written yet. Payout B's new
total is 145.

```sql
SELECT balance FROM driver_balances WHERE driver_id = 4471;
```

**3. A writes.**

```sql
UPDATE driver_balances SET balance = 160.00 WHERE driver_id = 4471;
```

**4. B writes.**

```sql
UPDATE driver_balances SET balance = 145.00 WHERE driver_id = 4471;
```

**5. Either terminal — look at the result.**

```sql
SELECT balance FROM driver_balances WHERE driver_id = 4471;
```

```
 balance
---------
  145.00
```

The driver is owed **€185** and the database says **€145**. Payout A's €40 is
gone. Both statements reported `UPDATE 1`. No error, no warning — the only
evidence is an underpaid driver.

## Round 2 — transactions, with a lock

Reset the balance (terminal A):

```sql
UPDATE driver_balances SET balance = 120.00 WHERE driver_id = 4471;
```

Same four steps, but each session now wraps its read and write in a transaction
and asks for the row `FOR UPDATE`, meaning: *give me this row, and let nobody
else touch it until I am done.*

**1. A takes the row.** A sees `120.00` and now holds a lock on it.

```sql
BEGIN;
SELECT balance FROM driver_balances WHERE driver_id = 4471 FOR UPDATE;
```

**2. B tries the same.**

```sql
BEGIN;
SELECT balance FROM driver_balances WHERE driver_id = 4471 FOR UPDATE;
```

**Watch terminal B.** No result, no prompt, no error — it just sits there,
waiting for A. **This pause is the exercise.** Leave it hanging and look at it.

**3. A writes and commits.**

```sql
UPDATE driver_balances SET balance = 160.00 WHERE driver_id = 4471;
COMMIT;
```

Now look at B again: its `SELECT` has returned, and it says `160.00` — not the
stale `120.00` it would have read a moment ago.

**4. B adds its €25 to what it actually read, and commits.**

```sql
UPDATE driver_balances SET balance = 185.00 WHERE driver_id = 4471;
COMMIT;
```

```
 balance
---------
  185.00
```

Nothing was lost. The cost was that B had to wait.

## Worth writing down

The two final balances, `145.00` and `185.00`, and one sentence on what would
have happened in round 1 if the payouts had arrived a minute apart instead of a
second apart.

> A single statement — `UPDATE driver_balances SET balance = balance + 40 WHERE
> driver_id = 4471` — is safe on its own, because the database does the arithmetic
> while holding the row. Applications rarely have that luxury: the amount usually
> depends on a rule, a rate, or a second table read in application code. That is
> why locks and transactions exist.

**If B did not wait:** both terminals must be in the same database, and A must
still be inside its transaction — if you committed A before B ran its
`SELECT … FOR UPDATE`, there is no lock left to wait for. Reset to 120 and start
round 2 again.
