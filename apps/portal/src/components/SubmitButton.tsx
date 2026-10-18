export function SubmitButton({
  pending,
  idle,
  busy,
}: {
  pending: boolean;
  idle: string;
  busy: string;
}) {
  return (
    <button
      type="submit"
      disabled={pending}
      className="mt-2 h-12 rounded-sm bg-linear-to-b from-[#e6c47e] to-[#b98f43] font-display text-[17px] font-extrabold tracking-wide text-night shadow-[inset_0_1px_0_rgb(255_255_255/0.35)] transition hover:brightness-110 disabled:cursor-wait disabled:opacity-70"
    >
      {pending ? busy : idle}
    </button>
  );
}

export function FormAlert({ message }: { message?: string }) {
  return (
    <p
      role="alert"
      aria-live="polite"
      className="text-sm text-ember empty:-mb-4"
    >
      {message}
    </p>
  );
}
