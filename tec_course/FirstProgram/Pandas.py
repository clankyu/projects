import pandas as p

df_students = p.read_csv("alumnos.csv")
print("Content of DataFrame df_students:")
print(df_students)

abscences = {
    "id" : [101, 102, 103, 104, 105],
    "abscences": [0, 2, 0, 3, 1]
}
df_abscences = p.DataFrame(abscences)
print("\nContent fo DataFrame df_absences:")
print(df_abscences)

df_combined = p.merge(df_students, df_abscences, on="id")
print("\nContent fo DataFrame combined:")
print(df_combined)

print("\nNumber of students per group:")
print(df_combined["grupo"].value_counts())

print("\nDataFrame sorted by grade (descending):")
print(df_combined.sort_values(by="nota", ascending=False))

print("\nStudents with grade less than 70:")
print(df_combined[df_combined["nota"] < 70])

print("\nAbscences of Martha:")
print(df_combined[df_combined["nombre"] == "Martha"]["abscences"].iloc[0])

df_combined.loc[df_combined["nombre"] == "Luis", "nota"] = 95

print("|Average of grades:")
print(df_combined["nota"].mean())

df_combined.to_csv("students_with_abscences.csv", index=False)

