interface Props {
  rationale: string;
}

export default function WhyDetails({ rationale }: Props) {
  return (
    <section className="card">
      <details>
        <summary>Zašto ove preporuke?</summary>
        <p>{rationale}</p>
      </details>
    </section>
  );
}
