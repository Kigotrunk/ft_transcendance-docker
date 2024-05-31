import axios from 'axios';
import React, { useEffect, useState } from 'react'

const Profile = () => {

  useEffect(() => {
    const getProfile = async () => {
      const res = await axios.get('http://localhost:8000/api/profile/1/');
      console.log(res);
    }
    getProfile();
  }, []);
  return (
	  <div>Profile</div>
  )
}

export default Profile;
