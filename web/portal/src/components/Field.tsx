import { type ComponentProps, useId } from "react";

type FieldProps = ComponentProps<"input"> & {
  label: string;
  hint?: string;
  error?: string;
};

export function Field({ label, hint, error, className, ...input }: FieldProps) {
  const id = useId();
  const describedBy = [hint && `${id}-hint`, error && `${id}-error`].filter(Boolean).join(" ") || undefined;
  return (
    <div className="flex flex-col gap-1.5">
      <label htmlFor={id} className="text-[13px] font-medium tracking-wide text-rice/85">
        {label}
      </label>
      <input
        id={id}
        aria-invalid={error ? true : undefined}
        aria-describedby={describedBy}
        className={`h-11 rounded-sm border border-gold/25 bg-night/70 px-3 text-[15px] text-rice placeholder:text-mist/50 transition-colors hover:border-gold/45 focus:border-gold focus:outline-none aria-invalid:border-ember ${className ?? ""}`}
        {...input}
      />
      {hint && !error && (
        <p id={`${id}-hint`} className="text-xs text-mist">
          {hint}
        </p>
      )}
      {error && (
        <p id={`${id}-error`} className="text-xs text-ember">
          {error}
        </p>
      )}
    </div>
  );
}
