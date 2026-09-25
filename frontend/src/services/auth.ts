import { 
  signInWithEmailAndPassword, 
  createUserWithEmailAndPassword, 
  signOut as firebaseSignOut
} from 'firebase/auth';
import { firebaseAuth } from '../config/firebase';
import { Role } from '../utils/roles';

export const login = async (email: string, password: string) => {
  const userCredential = await signInWithEmailAndPassword(firebaseAuth, email, password);
  return { user: userCredential.user };
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const register = async (email: string, password: string, profileData: any) => {
  const userCredential = await createUserWithEmailAndPassword(firebaseAuth, email, password);
  return { 
    user: userCredential.user, 
    role: Role.STUDENT,
    ...profileData 
  };
};

export const logout = async () => {
  await firebaseSignOut(firebaseAuth);
};
