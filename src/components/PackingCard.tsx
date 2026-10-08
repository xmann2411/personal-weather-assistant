interface Props {
  items: string[];
}

export default function PackingCard({ items }: Props) {
  return (
    <section className="card">
      <h3>Spakiraj</h3>
      {items.length === 0 ? (
        <p>Nema posebnih preporuka za pakiranje - osim dobre volje!</p>
      ) : (
        <ul>
          {items.map((item, i) => (
            <li key={i}>{item}</li>
          ))}
        </ul>
      )}
    </section>
  );
}
