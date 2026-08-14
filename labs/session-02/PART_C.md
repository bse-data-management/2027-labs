# Part C — The lost payout (8 min)

Two people write to the same row at the same time. No error is raised, and €40
disappears. You will make it happen, then stop it from happening.

You need **two terminals side by side**, both connected to the same database.
In each one, from the repository root, run:

```bash
docker compose exec postgres psql -U labs -d labs
```

Call the left terminal **A** and the right terminal **B**. Keep them both open
and visible — the whole lesson is in what terminal B does at one particular
moment.

---

## Setup (terminal A, once)

```sql
DROP TABLE IF EXISTS driver_balances;
CREATE TABLE driver_balances (
    driver_id integer PRIMARY KEY,
    balance   numeric(10,2) NOT NULL
);
INSERT INTO driver_balances VALUES (4471, 120.00);
SELECT * FROM driver_balances;
```

Driver 4471 has a balance of **€120**. Two payouts are about to arrive:
**payout A of €40** and **payout B of €25**. The driver is owed
120 + 40 + 25 = **€185**.

Notice that we type the *new total* in each `UPDATE` below, rather than writing
`balance = balance + 40`. That is not a trick to make the lab fail — it is what
almost every application does: read the balance, add the payout in Python, write
the result back. The addition happens outside the database.

---

## Round 1 — no transactions

Run these **in this exact order**, alternating terminals. Wait for each
statement to finish before moving to the next.

**Step 1 — A reads the balance**

```sql
SELECT balance FROM driver_balances WHERE driver_id = 4471;
```

A sees `120.00`. Payout A is €40, so A works out the new total: 160.

**Step 2 — B reads the balance**

```sql
SELECT balance FROM driver_balances WHERE driver_id = 4471;
```

B also sees `120.00` — A has not written anything yet. Payout B is €25, so B
works out the new total: 145.

**Step 3 — A writes**

```sql
UPDATE driver_balances SET balance = 160.00 WHERE driver_id = 4471;
```

**Step 4 — B writes**

```sql
UPDATE driver_balances SET balance = 145.00 WHERE driver_id = 4471;
```

**Step 5 — either terminal, check the result**

```sql
SELECT balance FROM driver_balances WHERE driver_id = 4471;
```

```
 balance
---------
  145.00
```

The driver is owed **€185** and the database says **€145**. Payout A's €40 is
gone. Both statements said `UPDATE 1`. No error, no warning, no log entry — the
only evidence is a driver who was underpaid.

---

## Round 2 — transactions, with a lock

Reset the balance (terminal A):

```sql
UPDATE driver_balances SET balance = 120.00 WHERE driver_id = 4471;
```

Now the same four steps, but each session wraps its read-and-write in a
transaction and asks for the row with `FOR UPDATE`, which means: *give me this
row and let nobody else touch it until I am done.*

**Step 1 — A opens a transaction and takes the row**

```sql
BEGIN;
SELECT balance FROM driver_balances WHERE driver_id = 4471 FOR UPDATE;
```

A sees `120.00`. A now holds a lock on that row.

**Step 2 — B tries to do the same**

```sql
BEGIN;
SELECT balance FROM driver_balances WHERE driver_id = 4471 FOR UPDATE;
```

**Watch terminal B.** Nothing happens. No result, no prompt, no error — it just
sits there. B is waiting for A to finish. **This pause is the point of the
exercise.** Leave it hanging and look at it for a moment.

**Step 3 — A writes and commits**

```sql
UPDATE driver_balances SET balance = 160.00 WHERE driver_id = 4471;
COMMIT;
```

Now look at terminal B again: the `SELECT` has returned, and it says `160.00` —
not the stale `120.00` it would have read a moment ago.

**Step 4 — B writes the correct total and commits**

B adds its €25 to what it actually read: 160 + 25 = 185.

```sql
UPDATE driver_balances SET balance = 185.00 WHERE driver_id = 4471;
COMMIT;
```

**Step 5 — check**

```sql
SELECT balance FROM driver_balances WHERE driver_id = 4471;
```

```
 balance
---------
  185.00
```

Nothing was lost. The cost was that terminal B had to wait.

---

## What to write down

1. The two final balances: `145.00` and `185.00`.
2. Roughly how long terminal B sat there waiting in round 2 — that waiting is
   the price of correctness, and it is why the next sessions care so much about
   how long a transaction stays open.
3. One sentence: what would have happened in round 1 if the two payouts had
   arrived a minute apart instead of a second apart?

> **Aside.** A single statement — `UPDATE driver_balances SET balance = balance +
> 40 WHERE driver_id = 4471` — is safe on its own, because the database does the
> arithmetic while holding the row. Real applications rarely have that luxury:
> the amount usually depends on a rule, a rate, or a second table read in
> application code. That is why locks and transactions exist.
