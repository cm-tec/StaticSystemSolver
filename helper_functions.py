import numpy as np


def delete_rows_and_columns_from_matrix(m, indices_to_delete):
    m = delete_columns_from_matrix(m, indices_to_delete)
    return delete_rows_from_matrix(m, indices_to_delete)


def delete_rows_from_matrix(m, indices_to_delete):
    return np.delete(m, indices_to_delete, axis=0)


def delete_columns_from_matrix(m, indices_to_delete):
    return np.delete(m, indices_to_delete, axis=1)
